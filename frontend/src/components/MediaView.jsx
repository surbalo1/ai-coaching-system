import { useState } from 'react';
import axios from 'axios';
import { Upload, Film, Scissors, CheckCircle, AlertCircle, Loader } from 'lucide-react';

const MediaView = () => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState("idle"); // idle, uploading, processing, done, error
    const [result, setResult] = useState(null);
    const [progress, setProgress] = useState(0);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setStatus("idle");
            setResult(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setStatus("uploading");
        const formData = new FormData();
        formData.append("file", file);

        try {
            // Simulated progress because axios upload progress is fast for local, 
            // but backend processing takes time.
            const interval = setInterval(() => {
                setProgress((prev) => (prev >= 90 ? 90 : prev + 10));
            }, 500);

            setStatus("processing");
            const res = await axios.post('/api/v1/media/process_video', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            clearInterval(interval);
            setProgress(100);
            setResult(res.data);
            setStatus("done");
        } catch (err) {
            console.error(err);
            setStatus("error");
        }
    };

    return (
        <div className="space-y-6">
            <header className="mb-8">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
                    Content Engine
                </h1>
                <p className="text-gray-400 mt-2">Upload long-form video, get viral clips automatically.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* Upload Area */}
                <div className="glass-panel p-8 flex flex-col items-center justify-center text-center border-dashed border-2 border-white/10 hover:border-red-500/50 transition-colors bg-white/5 relative">
                    <input
                        type="file"
                        accept="video/*"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div className="bg-red-500/20 p-4 rounded-full mb-4">
                        <Upload size={32} className="text-red-400" />
                    </div>
                    {file ? (
                        <div>
                            <p className="font-semibold text-white">{file.name}</p>
                            <p className="text-sm text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                    ) : (
                        <div>
                            <p className="font-semibold text-white">Drag & Drop Video</p>
                            <p className="text-sm text-gray-500">or click to browse (MP4, MOV)</p>
                        </div>
                    )}
                </div>

                {/* Status / Output Area */}
                <div className="glass-panel p-6 flex flex-col justify-center">

                    {status === 'idle' && (
                        <div className="text-center text-gray-500">
                            <Film size={48} className="mx-auto mb-4 opacity-20" />
                            <p>Ready to process.</p>
                            <button
                                onClick={handleUpload}
                                disabled={!file}
                                className="mt-6 btn-primary bg-gradient-to-r from-red-600 to-orange-600 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Start Processing
                            </button>
                        </div>
                    )}

                    {(status === 'uploading' || status === 'processing') && (
                        <div className="text-center">
                            <Loader size={48} className="mx-auto mb-4 text-red-500 animate-spin" />
                            <p className="text-lg font-medium text-white mb-2">
                                {status === 'uploading' ? 'Uploading...' : 'AI Analyzing Transcript...'}
                            </p>
                            <div className="w-full bg-white/10 rounded-full h-2 mt-4">
                                <div
                                    className="bg-red-500 h-2 rounded-full transition-all duration-500"
                                    style={{ width: `${progress}%` }}
                                ></div>
                            </div>
                        </div>
                    )}

                    {status === 'done' && result && (
                        <div className="animate-fade-in text-left">
                            <div className="flex items-center gap-2 mb-4 text-green-400">
                                <CheckCircle size={24} />
                                <h3 className="text-xl font-bold">Clip Generated!</h3>
                            </div>

                            <div className="bg-black/30 p-4 rounded-lg border border-white/10 mb-4">
                                <p className="text-sm text-gray-400 mb-1">Viral Reason:</p>
                                <p className="text-white italic">"{result.reason}"</p>
                            </div>

                            <div className="grid grid-cols-2 gap-4 text-sm mb-6">
                                <div className="bg-white/5 p-3 rounded">
                                    <span className="text-gray-500 block">Start Time</span>
                                    <span className="text-white font-mono">{result.start_time}</span>
                                </div>
                                <div className="bg-white/5 p-3 rounded">
                                    <span className="text-gray-500 block">End Time</span>
                                    <span className="text-white font-mono">{result.end_time}</span>
                                </div>
                            </div>

                            <a href={`http://localhost:8000${result.clip_path}`} target="_blank" rel="noopener noreferrer" className="block w-full text-center bg-white text-black font-bold py-3 rounded-lg hover:bg-gray-200 transition-colors">
                                <span className="flex items-center justify-center gap-2">
                                    <Scissors size={18} /> Download Clip
                                </span>
                            </a>
                        </div>
                    )}

                    {status === 'error' && (
                        <div className="text-center text-red-400">
                            <AlertCircle size={48} className="mx-auto mb-4" />
                            <p>Processing Failed.</p>
                            <button onClick={() => setStatus("idle")} className="mt-4 text-sm underline">Try Again</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default MediaView;
