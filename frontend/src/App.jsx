import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';

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

// Utility: get/set/remove token
function setToken(token) {
  localStorage.setItem('access_token', token);
}
function getToken() {
  return localStorage.getItem('access_token');
}
function removeToken() {
  localStorage.removeItem('access_token');
}

// Utility: decode JWT and check expiry
function isTokenExpired(token) {
  try {
    const decoded = jwt_decode(token);
    if (!decoded.exp) return true;
    return decoded.exp * 1000 < Date.now();
  } catch {
    return true;
  }
}

// Signup Page Component
function Signup() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
    role: 'admin',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const payload = {
        username: form.username,
        email: form.email,
        password: form.password,
        confirm_password: form.confirm_password,
        first_name: form.first_name,
        last_name: form.last_name,
        role: form.role,
      };
      const res = await axios.post(`${API_BASE}/auth/register`, payload);
      setSuccess(res.data.message || 'Registration successful!');
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1);
    } else {
      navigate('/');
    }
  };

  return (
    <div style={appStyle}>
      <div style={cardStyle}>
        <h2 style={{textAlign: 'center', marginBottom: '1rem'}}>Sign Up</h2>
        {error && <p style={{color: 'red'}}>{error}</p>}
        {success && <p style={{color: 'green'}}>{success}</p>}
        <form onSubmit={handleSubmit}>
          <input name="username" placeholder="Username" value={form.username} onChange={handleChange} required style={{width: '100%', marginBottom: 8, padding: 8}} />
          <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required style={{width: '100%', marginBottom: 8, padding: 8}} />
          <input name="first_name" placeholder="First Name" value={form.first_name} onChange={handleChange} style={{width: '100%', marginBottom: 8, padding: 8}} />
          <input name="last_name" placeholder="Last Name" value={form.last_name} onChange={handleChange} style={{width: '100%', marginBottom: 8, padding: 8}} />
          <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} required style={{width: '100%', marginBottom: 8, padding: 8}} />
          <input name="confirm_password" type="password" placeholder="Confirm Password" value={form.confirm_password} onChange={handleChange} required style={{width: '100%', marginBottom: 8, padding: 8}} />
          <select name="role" value={form.role} onChange={handleChange} style={{width: '100%', marginBottom: 8, padding: 8}}>
            <option value="admin">Admin</option>
            <option value="moderator">Moderator</option>
            <option value="super_admin">Super Admin</option>
          </select>
          <button type="submit" style={{...buttonStyle, width: '100%'}} disabled={loading}>{loading ? 'Registering...' : 'Sign Up'}</button>
        </form>
        <button onClick={handleBack} style={{...buttonStyle, width: '100%', marginTop: 8, background: '#888'}}>Back</button>
      </div>
    </div>
  );
}

// Login Page Component
function Login({ onLogin }) {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('username', form.username);
      params.append('password', form.password);
      const res = await axios.post(`${API_BASE}/auth/token`, params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        withCredentials: true,
      });
      setToken(res.data.access_token);
      setLoading(false);
      if (onLogin) onLogin();
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed.');
      setLoading(false);
    }
  };

  return (
    <div style={appStyle}>
      <div style={cardStyle}>
        <h2 style={{textAlign: 'center', marginBottom: '1rem'}}>Login</h2>
        {error && <p style={{color: 'red'}}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input name="username" placeholder="Username" value={form.username} onChange={handleChange} required style={{width: '100%', marginBottom: 8, padding: 8}} />
          <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} required style={{width: '100%', marginBottom: 8, padding: 8}} />
          <button type="submit" style={{...buttonStyle, width: '100%'}} disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
        </form>
      </div>
    </div>
  );
}

// QuizApp with session protection
function QuizApp({ onLogout, user, sessionMessage }) {
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
        {/* Navigation Links */}
        <nav style={{marginBottom: '1rem', textAlign: 'center'}}>
          <Link to="/" style={{marginRight: '1rem'}}>Quiz</Link>
          <Link to="/signup" style={{marginRight: '1rem'}}>Sign Up</Link>
          {!user && <Link to="/login">Login</Link>}
          {user && <button onClick={onLogout} style={{...buttonStyle, padding: '0.5rem 1rem', fontSize: '0.95rem'}}>Logout</button>}
          {user && (
            <span style={{marginLeft: 12, color: '#555', fontSize: '0.95rem'}}>
              {user.username} ({user.role})
            </span>
          )}
        </nav>
        {sessionMessage && (
          <div style={{color: '#d9534f', textAlign: 'center', marginBottom: 8}}>{sessionMessage}</div>
        )}
        {user ? (
          <>
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
          </>
        ) : (
          <div style={{textAlign: 'center', color: '#888', margin: '2rem 0'}}>
            <p>You must be logged in to access the quiz.</p>
            <Link to="/login">Go to Login</Link>
          </div>
        )}
      </div>
      <footer style={{marginTop: '2rem', color: '#888', fontSize: '0.95rem', textAlign: 'center'}}>
        &copy; {new Date().getFullYear()} Quiz App
      </footer>
    </div>
  );
}

// Main App with session logic and expiry handling
export default function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);
  const [sessionMessage, setSessionMessage] = useState('');

  // Helper: Try to refresh access token using cookie
  async function tryRefreshToken() {
    try {
      const res = await axios.post(`${API_BASE}/auth/refresh`, {}, { withCredentials: true });
      setToken(res.data.access_token);
      return true;
    } catch {
      removeToken();
      setUser(null);
      setSessionMessage('Session expired. Please log in again.');
      return false;
    }
  }

  // Check token on mount and at interval
  useEffect(() => {
    async function checkSession() {
      const token = getToken();
      if (token) {
        if (isTokenExpired(token)) {
          // Try to refresh
          const refreshed = await tryRefreshToken();
          if (!refreshed) {
            setChecking(false);
            return;
          }
        }
        // After refresh, get the (possibly new) token
        const validToken = getToken();
        axios.get(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${validToken}` },
        })
          .then(res => {
            setUser(res.data);
            setChecking(false);
          })
          .catch(() => {
            removeToken();
            setUser(null);
            setSessionMessage('Session expired or invalid. Please log in again.');
            setChecking(false);
          });
      } else {
        setChecking(false);
      }
    }
    checkSession();
    const interval = setInterval(checkSession, 60 * 1000); // check every 1 min
    return () => clearInterval(interval);
  }, []);

  const handleLogin = () => {
    const token = getToken();
    if (token) {
      if (isTokenExpired(token)) {
        tryRefreshToken().then(refreshed => {
          if (refreshed) {
            const validToken = getToken();
            axios.get(`${API_BASE}/auth/me`, {
              headers: { Authorization: `Bearer ${validToken}` },
            })
              .then(res => {
                setUser(res.data);
                setSessionMessage('');
              })
              .catch(() => {
                removeToken();
                setUser(null);
                setSessionMessage('Session expired or invalid. Please log in again.');
              });
          }
        });
      } else {
        axios.get(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
          .then(res => {
            setUser(res.data);
            setSessionMessage('');
          })
          .catch(() => {
            removeToken();
            setUser(null);
            setSessionMessage('Session expired or invalid. Please log in again.');
          });
      }
    }
  };

  const handleLogout = async () => {
    removeToken();
    setUser(null);
    setSessionMessage('You have been logged out.');
    try {
      await axios.post(`${API_BASE}/auth/logout`, {}, { withCredentials: true });
    } catch {}
  };

  if (checking) return <div style={appStyle}><div style={cardStyle}>Checking session...</div></div>;

  return (
    <Router>
      <Routes>
        <Route path="/" element={<QuizApp user={user} onLogout={handleLogout} sessionMessage={sessionMessage} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
      </Routes>
    </Router>
  );
}
