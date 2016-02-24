from bioseed import *
  
@app.route('/')
def mainIndex():
    return render_template('index.html')
    
@app.route('/search')
def search():
  return render_template('search.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080) 