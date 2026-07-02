# test_run.py
from src.data_engine import DataEngine

if __name__ == "__main__":
    ticker = "RELIANCE.NS"
    start_date = "2023-01-01"
    end_date = "2023-01-15"
    
    print("--- Booting Pattern Discovery Lab Data Engine ---")
    engine = DataEngine()
    
    # Execute the full ETL pipeline
    print(f"\n--- Executing Profiled Pipeline for {ticker} ---")
    context = engine.run_pipeline(ticker, start=start_date, end=end_date)
    
    # Interrogate the Pipeline Context
    print("\n=========================================")
    print("        PIPELINE CONTEXT STATE           ")
    print("=========================================")
    print(f"Ticker         : {context.ticker}")
    print(f"Source         : {context.source}")
    
    # --- AUDIT & TELEMETRY ---
    print("\n--- Audit & Lineage ---")
    print(f"Python Env     : {context.audit.python_version} ({context.audit.system_os})")
    print(f"Data Hash      : {context.audit.file_hash}")
    print(f"Total Time     : {context.audit.total_execution_ms} ms")
    
    if context.audit.step_times_ms:
        print("\nExecution Profile:")
        for step, ms in context.audit.step_times_ms.items():
            # Formatting to keep the columns perfectly aligned
            print(f"  - {step.ljust(15)}: {ms} ms")
            
    # --- VALIDATION REPORT ---
    if context.validation_report:
        print("\n--- Validation Report ---")
        print(f"Quality Score  : {context.validation_report.quality_score} / 100")
        print(f"Passed Critical: {context.validation_report.passed}")
        
        if context.validation_report.issues:
            print("\nIssues Detected:")
            for issue in context.validation_report.issues:
                print(f"  [{issue.severity.name}] {issue.rule_name}: {issue.message} ({issue.affected_rows} rows)")
        else:
            print("\nIssues Detected: None. Data is pristine.")
            
    # --- DATA PREVIEW ---
    print("\n--- Final Market Data Head ---")
    if context.market_data is not None:
        print(context.market_data.head())
    print("=========================================\n")