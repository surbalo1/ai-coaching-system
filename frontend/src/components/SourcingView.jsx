import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Play, UserCheck, Loader } from 'lucide-react';

const SourcingView = () => {
    const [rssUrl, setRssUrl] = useState("https://feeds.simplecast.com/54nAGcIl"); // Default content
    const [loading, setLoading] = useState(false);
    const [leads, setLeads] = useState([]);
    const [status, setStatus] = useState("");

    const fetchLeads = async () => {
        try {
            // In a real app, this would fetch from DB. For now, we mock or fetch from memory if endpoint exists.
            // Converting the backend's memory list to this view.
            const res = await axios.get('/api/v1/sourcing/leads');
            setLeads(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchLeads();
        // Poll every 5 seconds to mock real-time updates
        const interval = setInterval(fetchLeads, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleRun = async () => {
        setLoading(true);
        setStatus("🕵️‍♀️ AI Agent: Scanning Podcast Feed...");
        try {
            await axios.post('/api/v1/sourcing/run', null, { params: { rss_url: rssUrl } });
            setStatus("✅ Pipeline Triggered! Analyzing episodes in background...");
            // Reset status after a few seconds
            setTimeout(() => setStatus(""), 5000);
        } catch (err) {
            setStatus("❌ Error triggering agent.");
            console.error(err);
        }
        setLoading(false);
    };

    return (
        <div className="space-y-6">
            <header className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                        Speaker Sourcing
                    </h1>
                    <p className="text-gray-400 mt-2">Find high-ticket guests from podcasts automatically.</p>
                </div>
                <div className="bg-purple-900/30 px-4 py-2 rounded-lg border border-purple-500/30">
                    <span className="text-purple-300 font-mono text-sm">Target: Podcast RSS</span>
                </div>
            </header>

            {/* Input Section */}
            <div className="glass-panel p-6 flex gap-4 items-center">
                <div className="flex-1 bg-black/20 rounded-lg flex items-center px-4 border border-white/5 focus-within:border-purple-500 transition-colors">
                    <Search className="text-gray-500" size={20} />
                    <input
                        type="text"
                        value={rssUrl}
                        onChange={(e) => setRssUrl(e.target.value)}
                        placeholder="Enter Podcast RSS Feed URL..."
                        className="bg-transparent border-none outline-none text-white w-full p-3 ml-2"
                    />
                </div>
                <button
                    onClick={handleRun}
                    disabled={loading}
                    className="btn-primary flex items-center gap-2 disabled:opacity-50"
                >
                    {loading ? <Loader className="animate-spin" size={20} /> : <Play size={20} />}
                    Start Sourcing
                </button>
            </div>

            {status && (
                <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/20 text-green-300 flex items-center gap-2 animate-fade-in">
                    <span>{status}</span>
                </div>
            )}

            {/* Results Table */}
            <div className="glass-panel p-6 min-h-[400px]">
                <h3 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
                    <UserCheck className="text-purple-400" />
                    Detected Leads ({leads.length})
                </h3>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-white/10 text-gray-400 text-sm">
                                <th className="py-3 px-4">Guest Name</th>
                                <th className="py-3 px-4">Role / Company</th>
                                <th className="py-3 px-4">Score</th>
                                <th className="py-3 px-4">Status</th>
                                <th className="py-3 px-4">Action</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {leads.length === 0 ? (
                                <tr>
                                    <td colSpan="5" className="py-8 text-center text-gray-500 italic">
                                        No leads found yet. Start a search above.
                                    </td>
                                </tr>
                            ) : (
                                leads.map((lead, idx) => (
                                    <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                        <td className="py-3 px-4 font-medium text-white">{lead.name}</td>
                                        <td className="py-3 px-4 text-gray-400">{lead.role} @ {lead.company}</td>
                                        <td className="py-3 px-4">
                                            <span className={`px-2 py-1 rounded text-xs font-bold ${lead.score >= 8 ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                                                {lead.score}/10
                                            </span>
                                        </td>
                                        <td className="py-3 px-4">
                                            <span className="text-xs uppercase tracking-wider text-gray-500">{lead.status || 'NEW'}</span>
                                        </td>
                                        <td className="py-3 px-4">
                                            <button className="text-purple-400 hover:text-purple-300 text-xs underline">
                                                View Email
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default SourcingView;
