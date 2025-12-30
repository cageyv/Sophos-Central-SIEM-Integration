#!/usr/bin/env python3
"""
Wrapper script to run siem.py continuously.
Replaces cron-based execution with a simple loop.
"""
import sys
import time
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Execution interval in seconds (default: 10 minutes = 600 seconds)
INTERVAL = int(os.getenv('SIEM_INTERVAL', '600'))

def run_siem():
    """Execute siem.py main function and return exit code."""
    try:
        logging.info("Starting SIEM data collection...")
        
        # Import and run siem main function directly
        import siem
        siem.main()
        
        return 0
        
    except SystemExit as e:
        # Catch sys.exit() calls from siem.py
        return e.code if e.code else 0
    except Exception as e:
        logging.error(f"SIEM execution error: {e}", exc_info=True)
        return 1

def main():
    """Main loop to run siem.py continuously."""
    logging.info("Starting SIEM continuous execution wrapper")
    logging.info(f"Execution interval: {INTERVAL} seconds")
    
    while True:
        exit_code = run_siem()
        
        if exit_code == 0:
            logging.info(f"SIEM execution completed successfully. Sleeping {INTERVAL}s...")
        else:
            logging.warning(f"SIEM execution failed with code {exit_code}. Sleeping {INTERVAL}s...")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        sys.exit(0)

