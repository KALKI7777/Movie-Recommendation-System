from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the saved data
filters = pickle.load(open('V:\Bharat-Intern\Movie recomandation system\movies_recommended.pkl', 'rb'))
cosine_sim = pickle.load(open('V:\Bharat-Intern\Movie recomandation system\similarity.pkl', 'rb'))

def get_recommendations_new(title, cosine_sim=cosine_sim):
    title = title.replace(' ', '').lower()
    idx = filters[filters['title'].str.replace(' ', '').str.lower() == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return list(filters['title'].iloc[movie_indices])

@app.route('/')
def home():
    return render_template('index.html', result=[])

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        recommendations = get_recommendations_new(movie_name, cosine_sim=cosine_sim)
        return render_template('index.html', result=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
