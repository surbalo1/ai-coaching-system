import { BarChart3, Mail, MessageSquare, TrendingUp } from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, trend, color }) => (
    <div className="glass-panel p-6 flex items-start justify-between">
        <div>
            <p className="text-gray-400 text-sm font-medium mb-1">{label}</p>
            <h3 className="text-3xl font-bold text-white mb-2">{value}</h3>
            <div className={`flex items-center gap-1 text-xs ${trend.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>
                <TrendingUp size={12} />
                <span>{trend} vs last week</span>
            </div>
        </div>
        <div className={`p-3 rounded-lg bg-${color}-500/10 text-${color}-400`}>
            <Icon size={24} />
        </div>
    </div>
);

const OutreachView = () => {
    return (
        <div className="space-y-6">
            <header className="mb-8 flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                        Campaign Command Center
                    </h1>
                    <p className="text-gray-400 mt-2">Manage Cold Outreach & CRM Follow-ups.</p>
                </div>
                <button className="btn-primary bg-gradient-to-r from-green-600 to-emerald-600">
                    + New Campaign
                </button>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <StatCard icon={Mail} label="Emails Sent" value="1,248" trend="+12%" color="blue" />
                <StatCard icon={MessageSquare} label="Replies" value="86" trend="+5%" color="purple" />
                <StatCard icon={BarChart3} label="Conversion Rate" value="2.4%" trend="-0.1%" color="green" />
            </div>

            {/* Campaigns Table */}
            <div className="glass-panel p-6">
                <h3 className="text-xl font-semibold mb-6 text-white">Active Campaigns</h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-white/10 text-gray-500 text-sm">
                                <th className="py-4 font-medium">Campaign Name</th>
                                <th className="py-4 font-medium">Status</th>
                                <th className="py-4 font-medium">Prospects</th>
                                <th className="py-4 font-medium">Open Rate</th>
                                <th className="py-4 font-medium">Last Run</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            <tr className="border-b border-white/5 group hover:bg-white/5 transition-colors">
                                <td className="py-4 text-white font-medium">CEO Outreach - LinkedIn</td>
                                <td className="py-4"><span className="bg-green-500/20 text-green-400 px-2 py-1 rounded text-xs font-bold">ACTIVE</span></td>
                                <td className="py-4 text-gray-300">450</td>
                                <td className="py-4 text-gray-300">42%</td>
                                <td className="py-4 text-gray-400">2 mins ago</td>
                            </tr>
                            <tr className="border-b border-white/5 group hover:bg-white/5 transition-colors">
                                <td className="py-4 text-white font-medium">Podcast Guesting Q4</td>
                                <td className="py-4"><span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded text-xs font-bold">FINISHED</span></td>
                                <td className="py-4 text-gray-300">120</td>
                                <td className="py-4 text-gray-300">68%</td>
                                <td className="py-4 text-gray-400">Yesterday</td>
                            </tr>
                            <tr className="border-b border-white/5 group hover:bg-white/5 transition-colors">
                                <td className="py-4 text-white font-medium">Webinar Invite Sequence</td>
                                <td className="py-4"><span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded text-xs font-bold">PAUSED</span></td>
                                <td className="py-4 text-gray-300">890</td>
                                <td className="py-4 text-gray-300">--</td>
                                <td className="py-4 text-gray-400">Oct 24</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default OutreachView;
