const { useState } = React;

function App() {
    const [mode, setMode] = useState('encrypt');
    const [text, setText] = useState('');
    const [key, setKey] = useState('');
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAction = async () => {
        if (!text || !key) {
            setError('Please provide both text and key.');
            return;
        }
        
        setLoading(true);
        setError('');
        setResult('');

        try {
            const endpoint = mode === 'encrypt' ? '/api/encrypt' : '/api/decrypt';
            // Calling relative path as the backend will serve this frontend
            const apiUrl = endpoint;
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text, key })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'An error occurred');
            }

            const data = await response.json();
            setResult(data.result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(result);
        alert('Copied to clipboard!');
    };

    return (
        <div className="app-container">
            <header>
                <h1>Transposition Cipher</h1>
                <p className="subtitle">Secure your messages with columnar transposition</p>
            </header>

            <div className="tabs">
                <button 
                    className={`tab-btn ${mode === 'encrypt' ? 'active' : ''}`}
                    onClick={() => { setMode('encrypt'); setResult(''); setError(''); }}
                >
                    Encrypt
                </button>
                <button 
                    className={`tab-btn ${mode === 'decrypt' ? 'active' : ''}`}
                    onClick={() => { setMode('decrypt'); setResult(''); setError(''); }}
                >
                    Decrypt
                </button>
            </div>

            <div className="input-group">
                <label>Key</label>
                <input 
                    type="text" 
                    placeholder="Enter secret key (e.g., SECRET)" 
                    value={key}
                    onChange={(e) => setKey(e.target.value)}
                />
            </div>

            <div className="input-group">
                <label>{mode === 'encrypt' ? 'Plaintext' : 'Ciphertext'}</label>
                <textarea 
                    placeholder={`Enter text to ${mode}...`}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                />
            </div>

            {error && <div style={{ color: '#ef4444', marginBottom: '1rem', fontSize: '0.9rem' }}>{error}</div>}

            <button className="action-btn" onClick={handleAction} disabled={loading}>
                {loading ? 'Processing...' : (mode === 'encrypt' ? 'Encrypt Message' : 'Decrypt Message')}
            </button>

            {result && (
                <div className="result-box">
                    <button className="copy-btn" onClick={copyToClipboard}>Copy</button>
                    <h3>Result</h3>
                    <div className="result-text">{result}</div>
                </div>
            )}
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
