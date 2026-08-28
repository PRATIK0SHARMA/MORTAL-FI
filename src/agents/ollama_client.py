import json
from urllib import request
from urllib import error


# =================================================
# OLLAMA LOCAL LLM CLIENT
# =================================================

class OllamaClient:

    def __init__(

        self,

        model="qwen2.5:3b",

        host="http://localhost:11434"

    ):

        self.model = model

        self.host = host


    # =================================================
    # GENERATE RESPONSE
    # =================================================

    def generate(

        self,

        prompt,

        temperature=0.2

    ):

        url = (

            f"{self.host}/api/generate"

        )


        payload = {

            "model":
                self.model,


            "prompt":
                prompt,


            "stream":
                False,


            "options": {

                "temperature":
                    temperature

            }

        }


        try:

            # -----------------------------------------
            # CONVERT DATA TO JSON
            # -----------------------------------------

            request_data = (

                json.dumps(
                    payload
                )
                .encode(
                    "utf-8"
                )

            )


            # -----------------------------------------
            # CREATE HTTP REQUEST
            # -----------------------------------------

            http_request = (

                request.Request(

                    url,

                    data=request_data,

                    headers={

                        "Content-Type":
                            "application/json"

                    },

                    method="POST"

                )

            )


            # -----------------------------------------
            # SEND REQUEST TO OLLAMA
            # -----------------------------------------

            with request.urlopen(
                http_request,
                timeout=120
            ) as response:


                response_data = (

                    response.read()

                    .decode(
                        "utf-8"
                    )

                )


            # -----------------------------------------
            # PARSE RESPONSE
            # -----------------------------------------

            response_json = (

                json.loads(
                    response_data
                )

            )


            return (

                response_json.get(
                    "response"
                )

            )


        except error.URLError as exception:

            print(

                "\nOllama connection error:"

            )

            print(
                exception
            )


            return None


        except Exception as exception:

            print(

                "\nLLM generation error:"

            )

            print(
                exception
            )


            return None