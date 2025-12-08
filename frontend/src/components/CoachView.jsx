import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Paperclip } from 'lucide-react';

const CoachView = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am your AI Coach. I have access to your knowledge base. Ask me anything about your program.' }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const bottomRef = useRef(null);

    const scrollToBottom = () => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput("");
        setLoading(true);

        try {
            const res = await axios.post('/api/v1/coach/ask', { query: input });
            const aiMsg = { role: 'assistant', content: res.data.answer }; // Check API response structure
            setMessages(prev => [...prev, aiMsg]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: "⚠️ Error connecting to AI Coach." }]);
        }
        setLoading(false);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="h-[calc(100vh-100px)] flex flex-col">
            <header className="mb-6">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                    AI Conversational Coach
                </h1>
                <p className="text-gray-400">RAG System connected to your documents.</p>
            </header>

            {/* Chat Container */}
            <div className="flex-1 glass-panel flex flex-col overflow-hidden">
                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-purple-600' : 'bg-blue-600'}`}>
                                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                            </div>

                            <div className={`max-w-[70%] p-4 rounded-2xl ${msg.role === 'user'
                                    ? 'bg-purple-600/20 border border-purple-500/30 text-white rounded-tr-sm'
                                    : 'bg-white/5 border border-white/10 text-gray-200 rounded-tl-sm'
                                }`}>
                                <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex gap-4">
                            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center shrink-0">
                                <Bot size={16} />
                            </div>
                            <div className="bg-white/5 border border-white/10 px-4 py-3 rounded-2xl rounded-tl-sm">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></span>
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></span>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={bottomRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-white/10 bg-black/20">
                    <div className="flex gap-3">
                        <button className="p-3 text-gray-400 hover:text-white transition-colors">
                            <Paperclip size={20} />
                        </button>
                        <div className="flex-1 bg-white/5 rounded-xl border border-white/10 focus-within:border-blue-500/50 transition-colors flex items-center">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Ask about the coaching program..."
                                className="w-full bg-transparent border-none outline-none text-white px-4 py-3"
                            />
                        </div>
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || loading}
                            className="bg-blue-600 hover:bg-blue-500 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Send size={20} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CoachView;
