import React, { useEffect, useState } from "react";
import MdiEyeOff from "../icons/MdiEyeOff";
import MdiEye from "../icons/MdiEye";
import { useForm, type SubmitHandler, Form } from "react-hook-form";
import { cn } from "../../lib/utils";
import Cookies from "universal-cookie";
import { cookies } from "../../lib/cookies";

type TLogin = {
  username: string;
  password: string;
};

export default function LoginForm() {
  const [seePassword, setSeePassword] = useState<boolean>(false);

  const {
    register,
    formState: { errors },
    handleSubmit,
    watch,
  } = useForm<TLogin>();

  const onSubmit: SubmitHandler<TLogin> = async (data) => {
    await fetch(`http://localhost:8001/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      },
      body: new URLSearchParams({
        username: data.username,
        password: data.password,
      }),
    })
      .then(async (res) => {
        const data = (await res.json()) as {
          token_type: string;
          access_token: string;
        };
        cookies.set("isLoggedin", true);
        cookies.set("access_token", data.access_token);
        cookies.set("token_type", data.token_type);
        window.location.replace("/");
      })
      .catch((error) => {
        console.log("error");
      });
  };

  return (
    <div className="border py-5 px-8 rounded-md w-[480px] bg-white shadow-sm">
      <div>
        <h1 className="text-2xl font-semibold">Login</h1>
        <p className="text-sm text-gray-700">
          Login to continue using this app
        </p>
      </div>
      <hr className="my-5" />
      <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
        <div className="space-y-1">
          <label htmlFor="username" className="font-light">
            Username
          </label>
          <input
            type="text"
            id="username"
            placeholder="Dave"
            {...register("username", { minLength: 3 })}
            className={cn(
              "block border px-3 py-2 rounded-md w-full",
              errors.username && "border-rose-500"
            )}
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="password" className="font-light">
            Password
          </label>
          <div className="relative">
            <input
              type={seePassword ? "text" : "password"}
              id="password"
              placeholder="******"
              className={cn(
                "block border px-3 py-2 rounded-md w-full",
                errors.password && "border-rose-500"
              )}
              {...register("password", { minLength: 6 })}
            />

            <button
              type="button"
              className="absolute -translate-y-2/4 right-3 top-2/4"
              onClick={() => setSeePassword((password) => !password)}
            >
              {seePassword ? (
                <MdiEyeOff className="w-5 h-5 text-gray-700" />
              ) : (
                <MdiEye className="w-5 h-5 text-gray-700" />
              )}
            </button>
          </div>
        </div>
        <button
          type="submit"
          className="border rounded-md p-2 w-full hover:bg-green-400 bg-green-200 font-bold hover:text-white"
        >
          Login
        </button>
      </form>
    </div>
  );
}
