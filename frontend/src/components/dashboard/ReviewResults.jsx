
import ReactMarkdown from "react-markdown";

function ReviewResults({ reviewResult }) {
    if (!reviewResult) {
        return (
            <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
                <div className="border-b border-slate-100 px-5 py-4">
                    <h2 className="text-base font-semibold text-slate-900">
                        Review Results
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">
                        Consolidated findings and final recommendation
                    </p>
                </div>

                <div className="flex min-h-48 flex-col items-center justify-center px-5 py-10 text-center">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-xl text-slate-400">
                        ≡
                    </div>

                    <h3 className="text-sm font-semibold text-slate-800">
                        No review results yet
                    </h3>

                    <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
                        Submit a Git diff to see the analysis and final recommendation.
                    </p>
                </div>
            </section>
        );
    }

    const isApproved = reviewResult.recommendation === "approve";

    // Remove unnecessary backslashes before Markdown characters.
    const formattedReport = (reviewResult.final_report || "No report available.")
        .replace(/\\([*`_#|])/g, "$1");

    return (
        <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 px-5 py-4">
                <div>
                    <h2 className="text-base font-semibold text-slate-900">
                        Review Results
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">
                        Repository: {reviewResult.repository_name}
                    </p>
                </div>

                <span className={`rounded-md border px-3 py-1.5 text-xs font-semibold ${
                    isApproved
                        ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                        : "border-red-200 bg-red-50 text-red-700"
                }`}>
                    {isApproved ? "Approved" : "Changes Requested"}
                </span>
            </div>

            <div className="space-y-4 p-5">
                <div className="flex flex-wrap gap-6">
                    <div>
                        <p className="text-xs text-slate-500">Review ID</p>
                        <p className="mt-1 text-sm font-semibold text-slate-800">
                            #{reviewResult.review_id}
                        </p>
                    </div>

                    <div>
                        <p className="text-xs text-slate-500">Status</p>
                        <p className="mt-1 text-sm font-semibold capitalize text-slate-800">
                            {reviewResult.status}
                        </p>
                    </div>
                </div>

                <div>
                    <h3 className="mb-3 text-sm font-semibold text-slate-800">
                        Final Review Report
                    </h3>

                    <div className="rounded-md border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700
                        [&_h1]:mb-3 [&_h1]:text-lg [&_h1]:font-bold
                        [&_h2]:mb-2 [&_h2]:mt-4 [&_h2]:text-base [&_h2]:font-semibold
                        [&_h3]:mb-2 [&_h3]:mt-3 [&_h3]:font-semibold
                        [&_strong]:font-semibold [&_strong]:text-slate-900
                        [&_ul]:my-2 [&_ul]:list-disc [&_ul]:pl-6
                        [&_ol]:my-2 [&_ol]:list-decimal [&_ol]:pl-6
                        [&_li]:my-1
                        [&_code]:rounded [&_code]:bg-slate-200 [&_code]:px-1 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-xs
                        [&_table]:my-3 [&_table]:w-full [&_table]:border-collapse
                        [&_th]:border [&_th]:border-slate-300 [&_th]:bg-slate-100 [&_th]:p-2 [&_th]:text-left
                        [&_td]:border [&_td]:border-slate-300 [&_td]:p-2
                        [&_p]:my-2">
                        <ReactMarkdown>
                            {formattedReport}
                        </ReactMarkdown>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default ReviewResults;
