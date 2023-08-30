using Scheduler;
using Serilog;
using Quartz;
using Quartz.Impl;
using Quartz.Spi;
using System.Collections.Specialized;
using Quartz.Impl.AdoJobStore.Common;
using PythonScriptSchedulerService;

Log.Logger = new LoggerConfiguration()
                .MinimumLevel.Information()
                .WriteTo.File(
                    Path.Combine(
                        Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                        "LinkedIn",
                        "log-.log"
                    ), rollingInterval: RollingInterval.Day
                 )
                .CreateLogger();

Log.Logger.Information("Building host");
var host = Host
    .CreateDefaultBuilder(args)
    .ConfigureHostConfiguration(configHost =>
    {
        configHost.SetBasePath(Directory.GetCurrentDirectory());
        configHost.AddJsonFile("appsettings.json", optional: true);
    })
    .ConfigureServices((hostContext, services) =>
    {
        IConfiguration configuration = hostContext.Configuration;
        services.AddSingleton(configuration);
        services.AddSingleton<IDbProvider, CustomSqlServerConnectionProvider>();
        services.AddSingleton<ISchedulerFactory>((x) =>
        {
            var section = configuration.GetSection("Quartz");
            var nameValueCollection = new NameValueCollection();

            foreach (var child in section.GetChildren())
            {
                nameValueCollection.Add(child.Key, child.Value);
            }

            return new StdSchedulerFactory(nameValueCollection);
        });
        services.AddSingleton<PythonScriptScheduler>();
        services.AddTransient<PythonScriptJob>();
        services.AddSingleton<IJobFactory, SingletonJobFactory>();
        services.AddSingleton<PythonScriptScheduler>();
        services.AddHostedService<Worker>();
    })
    .UseWindowsService()
    .Build();

Log.Logger.Information("Run host");

await host.RunAsync();

Log.CloseAndFlush();
