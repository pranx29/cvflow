import JobApplication from "./pages/JobApplicationForm";

function App() {
    return (
        <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
                        Job Application
                    </h1>
                    <p className="mt-3 text-lg text-gray-600">
                        Please fill out the form below to apply for the position
                    </p>
                </div>
                <JobApplication />
            </div>
        </main>
    );
}

export default App;
