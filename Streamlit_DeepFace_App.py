{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/vazir0028/emoplay/blob/main/Streamlit_DeepFace_App.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import cv2\n",
        "import numpy as np\n",
        "from deepface import DeepFace\n",
        "from PIL import Image\n",
        "\n",
        "# 1. Set Page Configuration\n",
        "st.set_page_config(page_title=\"Emotion Music Recommender\", page_icon=\"🎵\")\n",
        "\n",
        "st.title(\"🎵 Emotion Based Music Recommendation\")\n",
        "st.write(\"This app uses DeepFace to detect your emotion and recommend music.\")\n",
        "\n",
        "# 2. Camera Input\n",
        "# Streamlit has a built-in camera input widget that is easier to use in Cloud than cv2.VideoCapture\n",
        "img_file_buffer = st.camera_input(\"Take a picture\")\n",
        "\n",
        "if img_file_buffer is not None:\n",
        "    # Convert the file to an opencv image.\n",
        "    bytes_data = img_file_buffer.getvalue()\n",
        "    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)\n",
        "\n",
        "    # Display processing message\n",
        "    with st.spinner('Analyzing emotion... (This might take a moment)'):\n",
        "        try:\n",
        "            # 3. Analyze Emotion\n",
        "            # enforce_detection=False prevents crash if face isn't perfect\n",
        "            result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)\n",
        "\n",
        "            # DeepFace returns a list of dictionaries in newer versions\n",
        "            if isinstance(result, list):\n",
        "                result = result[0]\n",
        "\n",
        "            dominant_emotion = result['dominant_emotion']\n",
        "\n",
        "            st.success(f\"Detected Emotion: **{dominant_emotion.upper()}**\")\n",
        "\n",
        "            # 4. Logic for Spotify (Placeholder)\n",
        "            st.subheader(f\"Recommended Playlist for {dominant_emotion}:\")\n",
        "            if dominant_emotion == 'happy':\n",
        "                st.write(\"🎶 Playing 'Happy Hits'...\")\n",
        "                # Add your Spotify logic here\n",
        "            elif dominant_emotion == 'sad':\n",
        "                st.write(\"🎶 Playing 'Melancholy Mix'...\")\n",
        "            else:\n",
        "                st.write(f\"🎶 Playing {dominant_emotion} vibes...\")\n",
        "\n",
        "        except Exception as e:\n",
        "            st.error(f\"Error analyzing face: {e}\")\n",
        "            st.info(\"Please make sure your face is clearly visible.\")"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "id": "OR_YNbeBaUou"
      }
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}