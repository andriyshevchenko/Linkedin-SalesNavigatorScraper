using Quartz;
using System.Diagnostics;
using static PythonScriptScheduler;

public class PythonScriptJob : IJob
{
    private readonly List<ScriptConfiguration> scriptConfigurations;
    private readonly ILogger<PythonScriptJob> logger;

    public PythonScriptJob(IConfiguration configuration, ILogger<PythonScriptJob> logger)
    {
        scriptConfigurations = configuration.GetSection("PythonScriptScheduler:Scripts")
            .Get<List<ScriptConfiguration>>();
        this.logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        try
        {
            foreach (var scriptConfig in scriptConfigurations)
            {
                // Use scriptConfig.ScriptPath and scriptConfig.CronExpression here
                // ... execute the Python script based on the configuration ...

                var processInfo = new ProcessStartInfo
                {
                    FileName = @"C:\Program Files\Python311\python.exe",
                    Arguments = scriptConfig.ScriptPath,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = new Process { StartInfo = processInfo })
                {
                    logger.LogInformation("Job execution started for script: {ScriptPath}", scriptConfig.ScriptPath);
                    process.Start();
                    await process.WaitForExitAsync();
                    logger.LogInformation("Job execution completed for script: {ScriptPath}", scriptConfig.ScriptPath);
                }
            }
        }
        catch (Exception ex)
        {
            // Handle exceptions
            logger.LogInformation("Error running script: {ex}", ex);
        }
    }
}
