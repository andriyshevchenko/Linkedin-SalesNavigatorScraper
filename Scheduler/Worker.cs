namespace Scheduler
{
    public class Worker : BackgroundService
    {
        private readonly ILogger<Worker> _logger;
        private readonly PythonScriptScheduler scheduler;

        public Worker(ILogger<Worker> logger, PythonScriptScheduler scheduler)
        {
            _logger = logger;
            this.scheduler = scheduler;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            await scheduler.Start(stoppingToken);

            while (!stoppingToken.IsCancellationRequested)
            {
                _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);
                await Task.Delay(1000, stoppingToken);
            }

            await scheduler.Stop(stoppingToken);
        }
    }
}