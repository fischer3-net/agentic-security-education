"""
Run All Stage 2 Demonstrations
===============================

This script runs all Stage 2 demonstrations in sequence:
1. Token Exchange Service Demo
2. Audit Logger Demo
3. Improved Agents Demo
4. Bearer Token Theft Exploit
5. Symmetric Key Compromise Exploit

Shows improvements over Stage 1 and remaining vulnerabilities.
"""

import asyncio
import subprocess
import sys
from pathlib import Path


class Stage2DemoRunner:
    """Runs all Stage 2 demonstrations in sequence."""
    
    def __init__(self):
        self.stage2_dir = Path(__file__).parent
        self.demos = [
            {
                "name": "Token Exchange Service Demo",
                "script": "token_exchange_service.py",
                "description": "Shows OAuth 2.0 style token exchange with audience restriction and scope downscoping"
            },
            {
                "name": "Audit Logger Demo",
                "script": "audit_logger.py",
                "description": "Demonstrates structured logging with correlation IDs and token lineage"
            },
            {
                "name": "Improved Agents Demo",
                "script": "improved_agents.py",
                "description": "Shows agents using token exchange instead of naive forwarding"
            },
            {
                "name": "Exploit 1: Bearer Token Theft",
                "script": "exploits/bearer_token_theft.py",
                "description": "Demonstrates that bearer tokens can still be stolen and used (HIGH severity)"
            },
            {
                "name": "Exploit 2: Symmetric Key Compromise",
                "script": "exploits/symmetric_key_still_broken.py",
                "description": "Shows that key compromise is still catastrophic (CATASTROPHIC severity)"
            }
        ]
    
    def print_header(self):
        """Print welcome header."""
        print("\n" + "="*70)
        print("STAGE 2: IMPROVED IMPLEMENTATION - ALL DEMONSTRATIONS")
        print("="*70)
        print()
        print("⚠️  This code is IMPROVED but still VULNERABLE!")
        print("   Better than Stage 1, but NOT production-ready.")
        print()
        print(f"Total demonstrations: {len(self.demos)}")
        print()
        print("="*70 + "\n")
    
    def print_demo_header(self, demo_num: int, demo: dict):
        """Print header for each demo."""
        print("\n" + "="*70)
        print(f"DEMO {demo_num}/{len(self.demos)}: {demo['name']}")
        print("="*70)
        print(f"Description: {demo['description']}")
        print(f"Script: {demo['script']}")
        print("="*70 + "\n")
    
    def wait_for_continue(self, demo_num: int):
        """Wait for user to press Enter before continuing."""
        if demo_num < len(self.demos):
            print("\n" + "-"*70)
            input("Press Enter to continue to next demonstration...")
            print("-"*70 + "\n")
    
    async def run_demo(self, demo_num: int, demo: dict) -> bool:
        """
        Run a single demonstration.
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.print_demo_header(demo_num, demo)
        
        script_path = self.stage2_dir / demo['script']
        
        if not script_path.exists():
            print(f"❌ ERROR: Script not found: {script_path}")
            return False
        
        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.stage2_dir,
                capture_output=False,  # Show output in real-time
                text=True
            )
            
            if result.returncode == 0:
                print(f"\n✅ {demo['name']} completed successfully")
                return True
            else:
                print(f"\n❌ {demo['name']} failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error running {demo['name']}: {e}")
            return False
    
    async def run_all(self, pause_between: bool = True):
        """
        Run all demonstrations in sequence.
        
        Args:
            pause_between: If True, wait for Enter between demos
        """
        self.print_header()
        
        results = []
        
        for i, demo in enumerate(self.demos, 1):
            success = await self.run_demo(i, demo)
            results.append((demo['name'], success))
            
            if pause_between and i < len(self.demos):
                self.wait_for_continue(i)
        
        # Print summary
        self.print_summary(results)
    
    def print_summary(self, results: list):
        """Print summary of all demonstrations."""
        print("\n" + "="*70)
        print("DEMONSTRATION SUMMARY")
        print("="*70)
        print()
        
        for name, success in results:
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{status}: {name}")
        
        print()
        
        successful = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"Completed: {successful}/{total} demonstrations")
        print()
        
        if successful == total:
            print("🎉 All demonstrations completed successfully!")
        else:
            print("⚠️  Some demonstrations failed. Check output above for details.")
        
        print()
        print("="*70)
        print()
        print("KEY TAKEAWAYS FROM STAGE 2:")
        print("="*70)
        print()
        print("✅ IMPROVEMENTS:")
        print("  • Token exchange instead of naive forwarding")
        print("  • Audience restriction blocks cross-service misuse")
        print("  • Automatic scope downscoping limits damage")
        print("  • 15-minute expiration (96% shorter than Stage 1)")
        print("  • Correlation IDs enable request tracing")
        print("  • Token lineage shows delegation chain")
        print("  • Structured audit logging improves forensics")
        print()
        print("⚠️  REMAINING VULNERABILITIES:")
        print("  • Symmetric keys (shared secret problem)")
        print("  • Bearer tokens (no proof-of-possession)")
        print("  • No replay protection (no nonce/jti)")
        print("  • Weak log integrity (MD5 checksums)")
        print("  • No token revocation mechanism")
        print()
        print("📊 IMPACT:")
        print("  • Better than Stage 1: YES")
        print("  • Production-ready: NO")
        print("  • Key lesson: 'Better' ≠ 'Secure Enough'")
        print()
        print("🚀 NEXT STEPS:")
        print("  • Review the improvements in detail")
        print("  • Understand why some attacks still work")
        print("  • Compare to Stage 1 (see what changed)")
        print("  • Identify which issues are architectural")
        print("  • Get ready for Stage 3 (production-grade fixes)")
        print()
        print("="*70 + "\n")


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run all Stage 2 federated identity demonstrations"
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="Don't pause between demonstrations"
    )
    parser.add_argument(
        "--demo",
        type=int,
        choices=range(1, 6),
        help="Run a specific demonstration (1-5)"
    )
    
    args = parser.parse_args()
    
    runner = Stage2DemoRunner()
    
    if args.demo:
        # Run specific demo
        demo = runner.demos[args.demo - 1]
        runner.print_header()
        await runner.run_demo(args.demo, demo)
    else:
        # Run all demos
        await runner.run_all(pause_between=not args.no_pause)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstrations interrupted by user")
        print("="*70 + "\n")
        sys.exit(0)
