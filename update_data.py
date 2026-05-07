steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install requests
          # 必须有下面这一行，否则机器人会因为找不到 AI 库而“罢工”
          pip install google-generativeai

      - name: Run update script
        env:
          GOOGLE_API_KEY: ${{ secrets.GEMINI_KEY }}
        run: python update_data.py
