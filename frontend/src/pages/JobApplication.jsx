import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import InputField from "../components/InputField";
import FileUpload from "../components/FileUpload";
import SubmitButton from "../components/SubmitButton";
import { submitApplication } from "../services/api";
import { schema } from "../utils/validation";

const JobApplication = () => {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitStatus, setSubmitStatus] = useState(null);

    const {
        register,
        control,
        handleSubmit,
        formState: { errors },
    } = useForm({ resolver: yupResolver(schema) });

    const onSubmit = async (data) => {
        setIsSubmitting(true);
        setSubmitStatus(null);
        try {
            const formData = new FormData();
            formData.append("first_name", data.first_name);
            formData.append("last_name", data.last_name);
            formData.append("email", data.email);
            formData.append("phone", data.phone);
            formData.append("cv", data.cv ? data.cv[0] : null);
            formData.append(
                "timezone",
                Intl.DateTimeFormat().resolvedOptions().timeZone
            );

            const response = await submitApplication(formData);
            if (response.status === 201) {
                setSubmitStatus({
                    type: "success",
                    message: "Application submitted successfully!",
                });
            } else {
                setSubmitStatus({
                    type: "error",
                    message: "Error submitting application. Please try again.",
                });
            }
        } catch (error) {
            if (error.response) {
                if (error.response.status === 422) {
                    setSubmitStatus({
                        type: "error",
                        message: "Validation error. Please check your details.",
                    });
                } else if (error.response.status === 500) {
                    setSubmitStatus({
                        type: "error",
                        message:
                            "An error occurred while processing your application. Try again later.",
                    });
                } else {
                    setSubmitStatus({
                        type: "error",
                        message:
                            "An unexpected error occurred. Please try again.",
                    });
                }
            } else {
                setSubmitStatus({
                    type: "error",
                    message: "Network error. Please check your connection.",
                });
            }
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen text-text-primary p-4">
            <div className="w-full max-w-md bg-white p-6 rounded-xl shadow-lg space-y-6">
                <div>
                    <h1 className="text-xl sm:text-2xl font-bold">
                        Job Application
                    </h1>
                    <p className="text-xs sm:text-sm text-text-secondary">
                        Please fill out the form below to apply for the position
                    </p>
                </div>

                {submitStatus && (
                    <div
                        className={`p-3 rounded ${
                            submitStatus.type === "success"
                                ? "bg-green-100 text-green-800"
                                : "bg-red-100 text-red-800"
                        }`}
                    >
                        {submitStatus.message}
                    </div>
                )}

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <InputField
                            label="First Name"
                            type="text"
                            register={register}
                            name="first_name"
                            errors={errors}
                        />
                        <InputField
                            label="Last Name"
                            type="text"
                            register={register}
                            name="last_name"
                            errors={errors}
                        />
                    </div>

                    <InputField
                        label="Email"
                        type="email"
                        register={register}
                        name="email"
                        errors={errors}
                    />

                    <InputField
                        label="Phone"
                        type="text"
                        register={register}
                        name="phone"
                        errors={errors}
                    />

                    <FileUpload
                        label="CV"
                        name="cv"
                        errors={errors}
                        control={control}
                    />

                    <SubmitButton isSubmitting={isSubmitting} />
                </form>
            </div>
        </div>
    );
};

export default JobApplication;
