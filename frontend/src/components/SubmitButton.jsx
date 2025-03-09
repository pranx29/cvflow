import React from "react";

const SubmitButton = () => {
    return (
        <button
            type="submit"
            className="w-full bg-primary text-white p-2 rounded-lg hover:bg-primary/90 transition-colors duration-200"
        >
            Send Application
        </button>
    );
};

export default SubmitButton;
