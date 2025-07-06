import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

const appStyle = {
  minHeight: '100vh',
  background: '#f3f3f7',
  fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '2rem',
};

const cardStyle = {
  background: '#fff',
  borderRadius: '16px',
  boxShadow: '0 4px 24px rgba(0,0,0,0.07)',
  padding: '2rem',
  minWidth: '320px',
  maxWidth: '400px',
  margin: '1rem',
};

const buttonStyle = {
  background: '#444',
  color: '#fff',
  border: 'none',
  borderRadius: '8px',
  padding: '0.75rem 1.5rem',
  fontSize: '1rem',
  margin: '0.5rem 0',
  cursor: 'pointer',
  transition: 'background 0.2s',
};

const selectedButtonStyle = {
  ...buttonStyle,
  background: '#888',
};

function App() {
  const [step, setStep] = useState('category');
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch categories on load
  useEffect(() => {
    if (step === 'category') {
      setLoading(true);
      axios.get(`${API_BASE}/quiz/categories/`)
        .then(res => {
          setCategories(res.data);
          setLoading(false);
        })
        .catch(() => {
          setError('Failed to load categories.');
          setLoading(false);
        });
    }
  }, [step]);

  // Fetch questions when category selected
  useEffect(() => {
    if (step === 'quiz' && selectedCategory) {
      setLoading(true);
      axios.get(`${API_BASE}/quiz/questions/${selectedCategory.id}?limit=5`)
        .then(res => {
          setQuestions(res.data);
          setLoading(false);
        })
        .catch(() => {
          setError('Failed to load questions.');
          setLoading(false);
        });
    }
  }, [step, selectedCategory]);

  const handleCategorySelect = (cat) => {
    setSelectedCategory(cat);
    setStep('quiz');
    setAnswers({});
    setResult(null);
    setError('');
  };

  const handleAnswer = (qid, option) => {
    setAnswers(prev => ({ ...prev, [qid]: option }));
  };

  const handleSubmit = () => {
    setLoading(true);
    setError('');
    const payload = Object.entries(answers).map(([question_id, selected_answer]) => ({
      question_id: Number(question_id),
      selected_answer,
    }));
    axios.post(`${API_BASE}/quiz/submit/${selectedCategory.id}`, payload)
      .then(res => {
        setResult(res.data);
        setStep('result');
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to submit answers.');
        setLoading(false);
      });
  };

  const handleRestart = () => {
    setStep('category');
    setSelectedCategory(null);
    setQuestions([]);
    setAnswers({});
    setResult(null);
    setError('');
  };

  return (
    <div style={appStyle}>
      <div style={cardStyle}>
        <h1 style={{textAlign: 'center', marginBottom: '1.5rem', color: '#333'}}>Quiz App</h1>
        {loading && <p style={{textAlign: 'center'}}>Loading...</p>}
        {error && <p style={{color: 'red', textAlign: 'center'}}>{error}</p>}

        {/* Category Selection */}
        {step === 'category' && !loading && (
          <>
            <h2 style={{marginBottom: '1rem', color: '#444'}}>Select a Category</h2>
            {categories.map(cat => (
              <button
                key={cat.id}
                style={buttonStyle}
                onClick={() => handleCategorySelect(cat)}
              >
                {cat.name}
              </button>
            ))}
          </>
        )}

        {/* Quiz Questions */}
        {step === 'quiz' && !loading && questions.length > 0 && (
          <form onSubmit={e => { e.preventDefault(); handleSubmit(); }}>
            <h2 style={{marginBottom: '1rem', color: '#444'}}>{selectedCategory.name} Quiz</h2>
            {questions.map((q, idx) => (
              <div key={q.id} style={{marginBottom: '1.5rem'}}>
                <div style={{marginBottom: '0.5rem', fontWeight: 600}}>
                  {idx + 1}. {q.question_text}
                </div>
                <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                  {['A', 'B', 'C', 'D'].map(opt => (
                    <button
                      type="button"
                      key={opt}
                      style={answers[q.id] === opt ? selectedButtonStyle : buttonStyle}
                      onClick={() => handleAnswer(q.id, opt)}
                    >
                      {opt}. {q[`option_${opt.toLowerCase()}`]}
                    </button>
                  ))}
                </div>
              </div>
            ))}
            <button
              type="submit"
              style={{...buttonStyle, width: '100%', marginTop: '1rem', background: '#222'}}
              disabled={Object.keys(answers).length !== questions.length}
            >
              Submit Answers
            </button>
          </form>
        )}

        {/* Result */}
        {step === 'result' && result && (
          <div style={{textAlign: 'center'}}>
            <h2 style={{color: '#444'}}>Results</h2>
            <p style={{fontSize: '1.2rem', margin: '1rem 0'}}>You scored <b>{result.correct_answers}</b> out of <b>{result.total_questions}</b></p>
            <p style={{fontSize: '1.5rem', color: result.score_percentage >= 70 ? '#28a745' : '#dc3545'}}>
              {result.score_percentage}%
            </p>
            <button style={buttonStyle} onClick={handleRestart}>Try Another Quiz</button>
          </div>
        )}
      </div>
      <footer style={{marginTop: '2rem', color: '#888', fontSize: '0.95rem', textAlign: 'center'}}>
        &copy; {new Date().getFullYear()} Quiz App
      </footer>
    </div>
  );
}

export default App;
