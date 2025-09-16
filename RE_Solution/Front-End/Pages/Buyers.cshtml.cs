using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Front_End.Pages
{
    public class BuyersModel : PageModel
    {
        private readonly ILogger<BuyersModel> _logger;

        public BuyersModel(ILogger<BuyersModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }
    }

}
