# test_run.py
from src.data_engine import DataEngine

if __name__ == "__main__":
    ticker = "RELIANCE.NS"
    start_date = "2023-01-01"
    end_date = "2023-01-15"
    
    print("--- Booting Pattern Discovery Lab Data Engine ---")
    engine = DataEngine()
    
    # Execute the full ETL pipeline
    print(f"\n--- Executing Pipeline for {ticker} ---")
    context = engine.run_pipeline(ticker, start=start_date, end=end_date)
    
    # Interrogate the Pipeline Context
    print("\n=====================================")
    print("        PIPELINE CONTEXT STATE       ")
    print("=====================================")
    print(f"Ticker         : {context.ticker}")
    print(f"Source         : {context.source}")
    print(f"Execution Time : {context.execution_time_ms} ms")
    
    if context.raw_data is not None:
        print(f"Raw Data       : {len(context.raw_data)} rows fetched")
        
    if context.standardized_data is not None:
        print(f"Standard Data  : {len(context.standardized_data)} rows processed")
        
    if context.validation_report:
        print("\n--- Validation Report ---")
        print(f"Quality Score  : {context.validation_report.quality_score} / 100")
        print(f"Passed Critical: {context.validation_report.passed}")
        
        if context.validation_report.issues:
            print("\nIssues Detected:")
            for issue in context.validation_report.issues:
                # issue.severity is an Enum, so we print its name
                print(f"  [{issue.severity.name}] {issue.rule_name}: {issue.message} ({issue.affected_rows} rows)")
        else:
            print("\nIssues Detected: None. Data is pristine.")
            
    print("\n--- Final Standardized Head ---")
    if context.standardized_data is not None:
        print(context.standardized_data.head())
    print("=====================================\n")