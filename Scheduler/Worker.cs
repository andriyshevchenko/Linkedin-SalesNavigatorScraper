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
            try
            {
                await scheduler.Start(stoppingToken);

                while (!stoppingToken.IsCancellationRequested)
                {
                    await Task.Delay(TimeSpan.FromSeconds(1), stoppingToken);
                }

                await scheduler.Stop(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogInformation("Error: {ex}", ex);
            }
        }
    }
}