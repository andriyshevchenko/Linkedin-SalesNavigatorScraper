using Quartz;
using System.Diagnostics;
using System.Net;
using System.Net.NetworkInformation;

public class PythonScriptJob : IJob
{
    private readonly ILogger<PythonScriptJob> logger;

    public PythonScriptJob(ILogger<PythonScriptJob> logger)
    {
        this.logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        JobDataMap dataMap = context.MergedJobDataMap;
        var scriptPath = dataMap?.GetString("ScriptPath");

        logger.LogInformation("Job execution started for script: {ScriptPath}", scriptPath);

        if (!await IsConnectedToInternet())
        {
            logger.LogInformation("Internet connection must be available.");
            throw new Quartz.JobExecutionException("Internet connection must be available.");
        }
        await ExecuteCommand($"python \"{scriptPath}\"");
    }

    public static async Task<bool> IsConnectedToInternet()
    {
        try
        {
            using (var client = new HttpClient())
            using (var stream = await client.GetStreamAsync("https://www.google.com"))
            {
                return true;
            }
        }
        catch
        {
            return false;
        }
    }

    public async Task ExecuteCommand(string command)
    {
        var processStartInfo = new ProcessStartInfo();
        processStartInfo.FileName = "powershell.exe";
        processStartInfo.Arguments = $"-Command \"{command}\"";
        processStartInfo.UseShellExecute = true;
        processStartInfo.RedirectStandardOutput = false;
        processStartInfo.CreateNoWindow = false;

        using var process = new Process();
        process.StartInfo = processStartInfo;
        process.Start();
        logger.LogInformation("Process started.");
        await process.WaitForExitAsync();
        logger.LogInformation("Process quit.");
        string output = await process.StandardOutput.ReadToEndAsync();
        logger.LogInformation(output);
        output = await process.StandardError.ReadToEndAsync();
        logger.LogInformation(output);
    }

    public string ExecutablePath(string version)
    {
        var executable = $"Python{version}";
        var path = Environment.GetEnvironmentVariable("PATH")
            ?.Split(';')
            ?.FirstOrDefault(x => !string.IsNullOrEmpty(Path.GetDirectoryName(x))
                                  && new DirectoryInfo(Path.GetDirectoryName(x)).Name == executable
                                  && System.IO.File.Exists(Path.Combine(x, "python.exe"))
                                  && !x.Contains("Scripts"));
        if (string.IsNullOrWhiteSpace(path))
        {
            logger.LogInformation("No {executable} located", executable);
            throw new InvalidOperationException($"No {executable} located");
        }
        logger.LogInformation("Python path: {path}", path);
        return Path.Combine(path, "python.exe");
    }
}
