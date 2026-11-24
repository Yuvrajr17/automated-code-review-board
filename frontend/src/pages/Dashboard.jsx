
import { useState } from "react";

import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";
import ReviewForm from "../components/dashboard/ReviewForm";
import AgentPipeline from "../components/dashboard/AgentPipeline";
import ReviewResults from "../components/dashboard/ReviewResults";

function Dashboard() {
    const [reviewResult, setReviewResult] = useState(null);

    const handleReviewComplete = (result) => {
        setReviewResult(result);
    };

    return (
        <div className="flex min-h-screen bg-slate-100">
            <Sidebar />

            <main className="min-w-0 flex-1">
                <Topbar />

                <div className="mx-auto max-w-7xl space-y-6 p-5 md:p-8">
                    <section>
                        <p className="text-sm font-medium text-emerald-700">
                            DEVELOPER WORKSPACE
                        </p>

                        <h1 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
                            Automated Code Review
                        </h1>

                        <p className="mt-2 text-sm text-slate-500">
                            Submit your code changes for automated quality and security analysis.
                        </p>
                    </section>

                    <div className="grid grid-cols-1 items-start gap-6 xl:grid-cols-5">
                        <div className="xl:col-span-3">
                            <ReviewForm
                                onReviewComplete={handleReviewComplete}
                            />
                        </div>

                        <div className="xl:col-span-2">
                            <AgentPipeline />
                        </div>
                    </div>

                    <ReviewResults reviewResult={reviewResult} />
                </div>
            </main>
        </div>
    );
}

export default Dashboard;
