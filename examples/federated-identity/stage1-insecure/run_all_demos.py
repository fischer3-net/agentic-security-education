"""
Run All Demonstrations
=======================

This script runs all Stage 1 demonstrations in sequence:
1. Token Generator Demo
2. Naive Agents Demo
3. All 4 Exploits

Useful for presentations or comprehensive walkthroughs.
"""

import asyncio
import subprocess
import sys
from pathlib import Path


class DemoRunner:
    """Runs all demonstrations in sequence."""
    
    def __init__(self):
        self.stage1_dir = Path(__file__).parent
        self.demos = [
            {
                "name": "Token Generator Demo",
                "script": "token_generator.py",
                "description": "Shows insecure token generation and naive forwarding"
            },
            {
                "name": "Naive Agents Demo",
                "script": "naive_agents.py",
                "description": "Demonstrates agent interactions and confused deputy attack"
            },
            {
                "name": "Exploit 1: Confused Deputy",
                "script": "exploits/confused_deputy.py",
                "description": "Shows how Agent C can impersonate users"
            },
            {
                "name": "Exploit 2: Token Replay",
                "script": "exploits/token_replay.py",
                "description": "Demonstrates token interception and replay attacks"
            },
            {
                "name": "Exploit 3: Scope Escalation",
                "script": "exploits/scope_escalation.py",
                "description": "Shows privilege escalation via wildcard scopes"
            },
            {
                "name": "Exploit 4: Audit Evasion",
                "script": "exploits/audit_evasion.py",
                "description": "Demonstrates inadequate audit logging"
            },
            {
                "name": "Exploit 5: Token Leakage",
                "script": "exploits/token_leakage.py",
                "description": "Shows token exposure in logs, URLs, and error messages"
            },
            {
                "name": "Exploit 6: Symmetric Key Compromise",
                "script": "exploits/symmetric_key_compromise.py",
                "description": "Demonstrates catastrophic impact of compromised shared secret"
            }
        ]
    
    def print_header(self):
        """Print welcome header."""
        print("\n" + "="*70)
        print("STAGE 1: FEDERATED IDENTITY - ALL DEMONSTRATIONS")
        print("="*70)
        print()
        print("⚠️  WARNING: This code is intentionally insecure!")
        print("   Educational purposes only - DO NOT use in production!")
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
        
        script_path = self.stage1_dir / demo['script']
        
        if not script_path.exists():
            print(f"❌ ERROR: Script not found: {script_path}")
            return False
        
        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.stage1_dir,
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
        print("Next Steps:")
        print("  1. Review the vulnerabilities identified in each demo")
        print("  2. Read the Stage 1 README.md for detailed explanations")
        print("  3. Progress to Stage 2 to see improvements")
        print()
        print("Questions?")
        print("  - Review CWE references in each exploit")
        print("  - Check the implementation plan for Stage 2")
        print("  - Study RFCs 8693 (Token Exchange) and 9449 (DPoP)")
        print()
        print("="*70 + "\n")


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run all Stage 1 federated identity demonstrations"
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="Don't pause between demonstrations"
    )
    parser.add_argument(
        "--demo",
        type=int,
        choices=range(1, 9),
        help="Run a specific demonstration (1-8)"
    )
    
    args = parser.parse_args()
    
    runner = DemoRunner()
    
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