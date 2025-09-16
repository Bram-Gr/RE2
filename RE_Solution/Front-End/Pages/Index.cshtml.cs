using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Front_End.Pages
{
    public class IndexModel : PageModel
    {
        private readonly IWebHostEnvironment _env;
        private readonly ILogger<IndexModel> _logger;

        public List<string> ImagePaths { get; set; }

        public IndexModel(IWebHostEnvironment env, ILogger<IndexModel> logger)
        {
            _env = env;
            _logger = logger;
        }

        public void OnGet()
        {
            var assetsPath = Path.Combine(_env.WebRootPath, "assets");
            if (Directory.Exists(assetsPath))
            {
                ImagePaths = Directory.GetFiles(assetsPath)
                    .Where(f => f.EndsWith(".jpg") || f.EndsWith(".png") || f.EndsWith(".jpeg") || f.EndsWith(".gif") || f.EndsWith(".jfif"))
                    .Select(f => "/assets/" + Path.GetFileName(f))
                    .ToList();
            }
            else
            {
                ImagePaths = new List<string>();
            }
        }
    }
}
