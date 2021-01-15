from flask import Flask, render_template_string,request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

header = """
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>easy Python</title>
</head>
<body style=' display: flex;align-items: center;justify-content: center;background-color:darkcyan'>
<h1 style='text-align: center'>
  """
footer = """
</h1>
<!--SSTI fuck!!!-->
<!--./flag-->
<div style='font-size: 15px;position: absolute;top: 90% ;'>
   <footer  >
  <p >EasyPython | Copyright <a href='https://www.hsm.cool'>HSM</a></p>
  
  <p >Powered By <a href='https://github.com/pallets/flask'> Flask</a></p>
</footer>
</div>
  </body>
</html>
  """

def filtered(template):#备用
  blacklist = ["self.__dict__","url_for","config","<p style='color'>getitems<p>","../","process"]
  #blacklist = ['']
  for b in blacklist:
    if b in template:
      template=template.replace(b,"")

  return template

@app.route("/")
def index():
  global header
  global footer
  return header+"Are you know Python ?"+footer

@app.route("/<path:template>")
def template(template):
  global header
  global footer
  if len(template) > 500:
    return "???"
  if template in ['flag','config']:
    return render_template_string(header+"Fuck ,Flag not here!!!"+footer)
  return render_template_string(header+str(template)+footer)

if __name__ == '__main__':
  app.run()
