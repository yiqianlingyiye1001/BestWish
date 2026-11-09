# scripts/repro_bug001.py
import os, sys, httpx

BASE = os.getenv("BASE_URL", "http://localhost:3000")

def main() -> int:
    with httpx.Client(base_url=BASE, timeout=10) as c:
        r = c.post("/api/auth/getShortMs")
    print(r.status_code, r.text[:200])
    if r.status_code != 401:
        print(f"[BUG-001] 期望 401，实际 {r.status_code} → 缺陷复现")
        return 1
    print("[BUG-001] 已修复")
    return 0

if __name__ == "__main__":
    sys.exit(main())