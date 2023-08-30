using Quartz;
using Quartz.Spi;

public partial class PythonScriptScheduler
{
    private IScheduler scheduler;
    private readonly IConfiguration configuration;
    private readonly IJobFactory jobFactory;
    private readonly ISchedulerFactory schedulerFactory;
    private readonly ILogger<PythonScriptScheduler> logger;

    public PythonScriptScheduler(IConfiguration configuration, IJobFactory jobFactory, ISchedulerFactory schedulerFactory, ILogger<PythonScriptScheduler> logger)
    {
        this.configuration = configuration;
        this.jobFactory = jobFactory;
        this.schedulerFactory = schedulerFactory;
        this.logger = logger;
    }

    public async Task Start(CancellationToken cancellationToken)
    {
        var scriptConfigs = configuration.GetSection("PythonScriptScheduler:Scripts")
                                        ?.Get<List<ScriptConfiguration>>() ?? new List<ScriptConfiguration>();
        if (!scriptConfigs.Any())
        {
            logger.LogInformation("No scripts detected.");
        }

        scheduler = await schedulerFactory.GetScheduler(cancellationToken);
        scheduler.JobFactory = jobFactory;
        logger.LogInformation("Starting scheduler");
        await scheduler.Start(cancellationToken);

        if (configuration.GetValue<bool>("PythonScriptScheduler:ClearDbOnStartup"))
        {
            await scheduler.Clear(cancellationToken);
            logger.LogInformation("Deleted all scheduled jobs");
        }

        foreach (var scriptConfig in scriptConfigs)
        {
            if (string.IsNullOrWhiteSpace(scriptConfig.ScriptPath))
            {
                throw new InvalidOperationException("Script path is empty.");
            }

            string jobName = $"PythonScriptJob_{scriptConfig.ScriptPath}_{scriptConfig.CronExpression}";
            var jobKey = new JobKey(jobName, "PythonScripts");
            var jobDetail = await scheduler.GetJobDetail(jobKey, cancellationToken);
            var job = JobBuilder.Create<PythonScriptJob>()
                .UsingJobData(
                    new JobDataMap
                    {
                        { "ScriptPath", scriptConfig.ScriptPath }
                    })
                .WithIdentity(jobKey)
                .Build();

            var triggerName = $"PythonScriptTrigger_{scriptConfig.ScriptPath}_{scriptConfig.CronExpression}";
            var trigger = TriggerBuilder.Create()
                .WithIdentity(triggerName, "PythonScripts")
                .WithCronSchedule(scriptConfig.CronExpression, x => x.WithMisfireHandlingInstructionFireAndProceed())
                .Build();

            if (jobDetail != null)
            {
                logger.LogInformation("Updating job {job}", trigger.Key);
                await scheduler.UnscheduleJob(trigger.Key, cancellationToken);
            }

            await scheduler.ScheduleJob(job, trigger, cancellationToken);
            logger.LogInformation("Done updating job {job}", trigger.Key);
        }
    }

    public async Task Stop(CancellationToken cancellationToken)
    {
        await scheduler.Shutdown(cancellationToken);
    }
}