using Quartz;
using Quartz.Spi;
using Quartz.Util;

public partial class PythonScriptScheduler
{
    private IScheduler scheduler;
    private readonly List<ScriptConfiguration> scriptConfigurations;
    private readonly IJobFactory jobFactory;
    private readonly ISchedulerFactory schedulerFactory;
    private readonly ILogger<PythonScriptScheduler> logger;

    public PythonScriptScheduler(IConfiguration configuration, IJobFactory jobFactory, ISchedulerFactory schedulerFactory, ILogger<PythonScriptScheduler> logger)
    {
        scriptConfigurations = configuration.GetSection("PythonScriptScheduler:Scripts")
            .Get<List<ScriptConfiguration>>();
        this.jobFactory = jobFactory;
        this.schedulerFactory = schedulerFactory;
        this.logger = logger;
    }

    public async Task Start(CancellationToken cancellationToken)
    {
        logger.LogInformation("Starting scheduler");
        logger.LogInformation("Waiting 5 minutes to ensure all services are available");
        await Task.Delay(TimeSpan.FromSeconds(5), cancellationToken);
        try
        {
            scheduler = await schedulerFactory.GetScheduler(cancellationToken);
        }
        catch (Exception e)
        {

            throw;
        }
        scheduler.JobFactory = jobFactory;
        await scheduler.Start(cancellationToken);

        foreach (var scriptConfig in scriptConfigurations)
        {
            if (string.IsNullOrWhiteSpace(scriptConfig.ScriptPath))
            {
                throw new InvalidOperationException("Script path is empty.");
            }

            var jobData = new JobDataMap
            {
                { "ScriptPath", scriptConfig.ScriptPath }
            };

            var job = JobBuilder.Create<PythonScriptJob>()
                .WithIdentity($"PythonScriptJob_{scriptConfig.ScriptPath}", "PythonScripts")
                .StoreDurably(true)
                .UsingJobData(jobData)
                .Build();

            var trigger = TriggerBuilder.Create()
                .WithIdentity($"PythonScriptTrigger_{scriptConfig.ScriptPath}", "PythonScripts")
                .WithCronSchedule(scriptConfig.CronExpression, x => x.WithMisfireHandlingInstructionFireAndProceed())
                .Build();

            await scheduler.ScheduleJob(job, trigger, cancellationToken);
        }
    }

    public async Task Stop(CancellationToken cancellationToken)
    {
        await scheduler.Shutdown(cancellationToken);
    }   
}