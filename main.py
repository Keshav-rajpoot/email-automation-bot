from auto_reply import reply_flow
from logger import log_batch, summary_report

if __name__ == "__main__":
    # 1) DRY RUN: see what would happen
    #results = reply_flow(dry_run=True, max_results=10)
    #log_batch(results)
    #summary_report()

    # 2) When you're confident, flip to real sending:
     results = reply_flow(dry_run=False, max_results=10)
     log_batch(results)
     summary_report()
