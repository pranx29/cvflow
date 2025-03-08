import React from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import InputField from "../components/InputField";
import FileUpload from "../components/FileUpload";
import SubmitButton from "../components/SubmitButton";
import { submitApplication } from "../services/api";
import { schema } from "../utils/validation";

const JobApplication = () => {
    const {
        register,
        control,
        handleSubmit,
        formState: { errors },
    } = useForm({ resolver: yupResolver(schema) });

    const onSubmit = async (data) => {
        try {
            const formData = new FormData();
            formData.append("name", data.name);
            formData.append("email", data.email);
            formData.append("phone", data.phone);
            formData.append("cv", data.cv ? data.cv[0] : null);
            formData.append(
                "timezone",
                Intl.DateTimeFormat().resolvedOptions().timeZone
            );
            const response = await submitApplication(formData);

            if (response.status === 200) {
                alert("Application submitted successfully!");
            } else {
                console.log("Error:", response);
            }
        } catch (error) {
            console.log("Error uploading:", error);
            alert("Error submitting form. Please check your details.");
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <InputField
                label="Name"
                type="text"
                register={register}
                name="name"
                errors={errors}
            />
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
                label="Upload CV"
                name="cv"
                errors={errors}
                control={control}
            />
            <SubmitButton />
        </form>
    );
};

export default JobApplication;
