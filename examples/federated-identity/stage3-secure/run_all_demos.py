"""
Stage 3 - Run All Demonstrations
=================================

This script runs all Stage 3 demonstrations in sequence to showcase
the complete production-ready security implementation.

Total estimated time: 5-10 minutes
"""

import sys
import subprocess
from pathlib import Path


def print_banner(text, char="="):
    """Print a formatted banner."""
    width = 70
    print("\n" + char * width)
    print(text.center(width))
    print(char * width + "\n")


def run_demo(script_path, demo_name):
    """Run a demonstration script."""
    print_banner(f"DEMO: {demo_name}", "=")
    print(f"Running: {script_path}")
    print()
    
    # Get absolute path to script
    script_file = Path(__file__).parent / script_path
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_file)],
            cwd=Path(__file__).parent,  # Always run from stage3-secure directory
            check=True,
            text=True
        )
        
        print()
        print("✅ Demo completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print(f"❌ Demo failed with error code {e.returncode}")
        return False
    except Exception as e:
        print()
        print(f"❌ Demo failed: {e}")
        return False


def main():
    """Run all Stage 3 demonstrations."""
    
    print_banner("STAGE 3: COMPLETE DEMONSTRATION SUITE", "=")
    
    print("This will run all Stage 3 demonstrations sequentially.")
    print()
    print("Demonstrations included:")
    print("  1. Asymmetric Key Management")
    print("  2. DPoP Proof-of-Possession")
    print("  3. Secure Audit Logging")
    print("  4. W3C Trace Context")
    print("  5. Token Revocation")
    print("  6. Policy Engine")
    print("  7. Secure Agents")
    print("  8. Complete Secure Flow (interactive)")
    print("  9. Exploit: DPoP Blocks Token Theft")
    print(" 10. Exploit: Revocation Blocks Compromise")
    print(" 11. Exploit: Limited Key Compromise Impact")
    print()
    print("Estimated time: 5-10 minutes")
    print()
    
    response = input("Press Enter to begin, or 'q' to quit: ")
    if response.lower() == 'q':
        print("Exiting...")
        return
    
    # Track results
    results = {}
    
    # Define demonstrations
    demos = [
        ("key_manager.py", "Asymmetric Key Management"),
        ("dpop_token_service.py", "DPoP Proof-of-Possession"),
        ("secure_audit_logger.py", "Secure Audit Logging"),
        ("trace_context.py", "W3C Trace Context"),
        ("revocation_service.py", "Token Revocation"),
        ("policy_engine.py", "Policy Engine"),
        ("secure_agents.py", "Secure Agents"),
        ("demos/demo_full_flow.py", "Complete Secure Flow"),
        ("exploits/theft_fails_dpop.py", "Exploit: DPoP Blocks Theft"),
        ("exploits/revocation_blocks.py", "Exploit: Revocation Blocks"),
        ("exploits/key_compromise_limited.py", "Exploit: Limited Impact"),
    ]
    
    # Run each demo
    for script, name in demos:
        success = run_demo(script, name)
        results[name] = success
        
        if not success:
            print()
            response = input("Demo failed. Continue anyway? (y/n): ")
            if response.lower() != 'y':
                break
        
        print()
        input("Press Enter to continue to next demo...")
    
    # Print summary
    print_banner("DEMONSTRATION SUMMARY", "=")
    
    total = len(results)
    passed = sum(1 for success in results.values() if success)
    failed = total - passed
    
    print(f"Total demonstrations: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print()
    
    print("Results:")
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print()
    
    if failed == 0:
        print_banner("ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!", "*")
        print()
        print("You have seen:")
        print()
        print("✅ Asymmetric cryptography eliminating shared secrets")
        print("✅ DPoP proof-of-possession preventing token theft")
        print("✅ Secure audit logging with cryptographic signatures")
        print("✅ W3C Trace Context for distributed tracing")
        print("✅ Token revocation for immediate security response")
        print("✅ Policy engine for centralized authorization")
        print("✅ Complete production-ready secure flow")
        print("✅ Exploits demonstrating the defenses work")
        print()
        print("Stage 3 is PRODUCTION-READY! 🎉")
        print()
    else:
        print_banner("SOME DEMONSTRATIONS FAILED", "!")
        print()
        print("Please review the errors above.")
        print("Common issues:")
        print("  • Missing dependencies (run: pip install -r requirements.txt)")
        print("  • Python version < 3.8")
        print("  • File permissions")
        print()
    
    print_banner("END OF DEMONSTRATIONS", "=")


if __name__ == "__main__":
    main()