import config
import countries
import e404
import hall_of_fame
import homepage
import search
import static_files
import timeline

print("Generating the whole project")
homepage.run()
e404.run()
timeline.run()
countries.run()
search.run()
hall_of_fame.run()
static_files.run()

print("ALERT: adding preliminary results notice to timeline/2026")
notice = (
  '  <b>Preliminary Results:</b><br/>\n'
  '  Results shown are based mainly on the closing ceremony and other sources on the Internet.<br/>\n'
  '  Rankings reflect order of appearance at the closing ceremony.<br/>\n'
  f'  Please send any relevant corrections to the webmaster: <a href="mailto:{config.webmaster_email}">{config.webmaster_email}</a>\n'
)
for page in ["country", "individual"]:
  path = f"../timeline/2026/{page}.html"
  with open(path) as file:
    html = file.read()
  html = html.replace("  </h3>\n  <table>", "  </h3>\n" + notice + "  <table>", 1)
  with open(path, "w") as file:
    file.write(html)
