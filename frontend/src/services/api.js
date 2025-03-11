import axios from "axios";

export const submitApplication = async (formData) => {
    try {
        const response = await axios.post(
            "https://sportsync.live/api/job-application/submit",
            formData,
            {
                headers: { "Content-Type": "multipart/form-data" },
            }
        );
        return response;
    } catch (error) {
        throw error;
    }
};
