# EcoTrace testing checklist

Run:

```bash
python manage.py check
python manage.py makemigrations lifecycle
python manage.py migrate
python manage.py test
```

Manual acceptance test:

1. Open `/`.
2. Open `/assets/add/`.
3. Submit a Laptop with condition 9.
4. Confirm dashboard counts increase.
5. Confirm the decision is `CONTINUE` in fallback mode.
6. Submit another asset with condition 2.
7. Confirm the decision is `RECYCLE`.
8. Open `/assets/` and test search/filtering.
9. Open `/responsible-ai/` and verify governance sections.
10. If IBM credentials are configured, confirm the passport's AI source changes to IBM Granite via watsonx.ai.
