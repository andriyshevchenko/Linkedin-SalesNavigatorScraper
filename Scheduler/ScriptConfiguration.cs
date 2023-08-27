public partial class PythonScriptScheduler
{
    public class ScriptConfiguration
    {
        public string ScriptPath { get; set; }
        public string CronExpression { get; set; }
    }
}