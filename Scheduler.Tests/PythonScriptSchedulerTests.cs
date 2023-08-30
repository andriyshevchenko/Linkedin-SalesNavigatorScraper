using Microsoft.Extensions.Logging;
using Moq;

namespace Scheduler.Tests
{
    public class PythonScriptSchedulerTests
    {
        [Fact]
        public void ExecutablePath_Exists()
        {
            var sut = new PythonScriptJob(new Mock<ILogger<PythonScriptJob>>().Object);
            Assert.True(File.Exists(sut.ExecutablePath("311")));
        }
    }
}