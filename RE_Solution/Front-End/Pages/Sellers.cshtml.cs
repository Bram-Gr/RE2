using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Front_End.Pages
{
    public class SellersModel : PageModel
    {
        private readonly ILogger<SellersModel> _logger;

        public SellersModel(ILogger<SellersModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }
    }
}
