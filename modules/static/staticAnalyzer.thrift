service StaticAnalyze {
    string connect(),
    string analyze(1:string bin_path, 2:string report_path),
}