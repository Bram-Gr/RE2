using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace CompAnalysisService.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SearchPropertyController : Controller
    {
        private readonly IPropertyRepository _propertyRepository;

        public SearchPropertyController(IPropertyRepository propertyRepository)
        {
            _propertyRepository = propertyRepository;
        }

        // GET: api/SearchPropertyController/search?query={query}
        [HttpGet("search")]
        public async Task<IActionResult> Search([FromQuery] string query)
        {
            if (string.IsNullOrWhiteSpace(query) || query.Length < 1)
            {
                return BadRequest("Query must be at least 1 character long.");
            }

            var results = await _propertyRepository.SearchPropertiesAsync(query);
            return Ok(results);
        }

        // GET: SearchPropertyController
        public ActionResult Index()
        {
            return View();
        }

        // GET: SearchPropertyController/Details/5
        public ActionResult Details(int id)
        {
            return View();
        }

        // GET: SearchPropertyController/Create
        public ActionResult Create()
        {
            return View();
        }

        // POST: SearchPropertyController/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(IFormCollection collection)
        {
            try
            {
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }

        // GET: SearchPropertyController/Edit/5
        public ActionResult Edit(int id)
        {
            return View();
        }

        // POST: SearchPropertyController/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(int id, IFormCollection collection)
        {
            try
            {
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }

        // GET: SearchPropertyController/Delete/5
        public ActionResult Delete(int id)
        {
            return View();
        }

        // POST: SearchPropertyController/Delete/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Delete(int id, IFormCollection collection)
        {
            try
            {
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }
    }
}
