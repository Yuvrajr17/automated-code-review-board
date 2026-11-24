import { useState } from "react";
import { submitReview } from "../../services/reviewService";

function ReviewForm({ onReviewComplete }) {
    const [repositoryName, setRepositoryName] = useState("");
    const [diffText, setDiffText] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!repositoryName.trim()) {
        setError("Please enter a repository name.");
        return;
    }

    if (!diffText.trim()) {
        setError("Please paste a Git diff before submitting.");
        return;
    }

    setLoading(true);

    try {
        const result = await submitReview({
            repository_name: repositoryName.trim(),
            diff_text: diffText.trim(),
        });

        onReviewComplete(result);

    } catch (err) {
        console.error("Review submission error:", err);
        setError(err.message || "Something went wrong. Please try again.");
    } finally {
        setLoading(false);
    }
};

    return (
        <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
            {/* Section header */}
            <div className="border-b border-slate-100 px-5 py-4">
                <h2 className="text-base font-semibold text-slate-900">
                    New Code Review
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                    Provide repository details and your Git diff.
                </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5 p-5">
                <div>
                    <label
                        htmlFor="repository"
                        className="mb-2 block text-sm font-medium text-slate-700"
                    >
                        Repository name
                    </label>

                    <input
                        id="repository"
                        type="text"
                        value={repositoryName}
                        onChange={(e) => setRepositoryName(e.target.value)}
                        placeholder="e.g. ecommerce-backend"
                        className="w-full rounded-md border border-slate-300 px-3 py-2.5 text-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                    />
                </div>

                <div>
                    <div className="mb-2 flex items-center justify-between">
                        <label
                            htmlFor="git-diff"
                            className="text-sm font-medium text-slate-700"
                        >
                            Git diff
                        </label>

                        <span className="text-xs text-slate-400">
                            Unified diff format
                        </span>
                    </div>

                    <textarea
                        id="git-diff"
                        rows={12}
                        spellCheck={false}
                        value={diffText}
                        onChange={(e) => setDiffText(e.target.value)}
                        placeholder={`Paste your Git diff here...

                        diff --git a/example.py b/example.py
                        --- a/example.py
                        +++ b/example.py`}
                        className="w-full resize-y rounded-md border border-slate-300 bg-slate-50 p-4 font-mono text-xs leading-6 text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
                    />
                </div>

                {error && (
                    <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                        {error}
                    </p>
                )}

                <div className="flex flex-wrap items-center justify-between gap-3">
                    <p className="text-xs text-slate-400">
                        Submit a Git diff to start the five-agent review.
                    </p>

                    <button
                        type="submit"
                        disabled={loading}
                        className="rounded-md bg-emerald-700 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {loading ? "Preparing Review..." : "Run Code Review →"}
                    </button>
                </div>
            </form>
        </section>
    );
}

export default ReviewForm;
