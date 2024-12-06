import OpenAI from "openai";
import { StreamTextResult } from "ai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY }); // add the api key in the .env file

export async function POST(req: Request, res: Response) {
  const { messages } = await req.json();
  console.log(messages);
  const response = await openai.chat.completions.create({
    model: "gpt-4", //Change the model to your liking
    messages: [...messages],
    stream: true,
    temperature: 1,
  });

  return response;
}
