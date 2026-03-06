'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Activity, Heart, ShieldAlert } from 'lucide-react';

type Message = {
  role: 'user' | 'agent';
  content: string;
  type?: 'diagnosis' | 'plan' | 'safety';
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'agent', content: "Hello! I'm your Recovery Buddy. How are you feeling today? Please let me know if you have any mobility pain, dizziness, or breathlessness." }
  ]);
  const [input, setInput] = useState('');
  const [preference, setPreference] = useState<'short-term' | 'long-term'>('long-term');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput('');
    setMessages((prev: Message[]) => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage, preference }),
      });

      const data = await res.json();

      setMessages((prev: Message[]) => [
        ...prev,
        { role: 'agent', content: data.diagnosis, type: 'diagnosis' },
        { role: 'agent', content: data.recovery_plan, type: 'plan' },
        { role: 'agent', content: data.safety_check, type: 'safety' }
      ]);
    } catch (err) {
      setMessages((prev: Message[]) => [...prev, { role: 'agent', content: "Sorry, I'm having trouble connecting to my brain right now. Please ensure the backend is running." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="header">
        <h1>Rec-Buddy</h1>
        <p>Recovery Back to Fitness</p>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              {m.type === 'diagnosis' && <div className="status-badge" style={{color: '#6366f1'}}><Activity size={14} /> Diagnosis</div>}
              {m.type === 'plan' && <div className="status-badge" style={{color: '#ec4899'}}><Heart size={14} /> Recovery Plan</div>}
              {m.type === 'safety' && <div className="status-badge" style={{color: '#f59e0b'}}><ShieldAlert size={14} /> Safety Check</div>}
              {m.content}
            </div>
          ))}
          {loading && <div className="message agent">Processing feedback...</div>}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="preference-selector">
            <button 
              className={`preference-btn ${preference === 'short-term' ? 'active' : ''}`}
              onClick={() => setPreference('short-term')}
            >
              Short Term Relief
            </button>
            <button 
              className={`preference-btn ${preference === 'long-term' ? 'active' : ''}`}
              onClick={() => setPreference('long-term')}
            >
              Slow & Steady Progress
            </button>
          </div>
          
          <form onSubmit={handleSubmit} className="input-row">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Tell me how you feel... (e.g., knee pain, dizziness)"
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
