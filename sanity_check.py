import os
import sys
import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))

def section(title):
    print("\n" + "="*70)
    print(title)
    print("="*70)

def check_file(path):
    full = os.path.join(ROOT, path)
    exists = os.path.isfile(full)
    print(f"[{'OK' if exists else 'MISSING'}] {path}")
    return exists

def check_dir(path):
    full = os.path.join(ROOT, path)
    exists = os.path.isdir(full)
    print(f"[{'OK' if exists else 'MISSING'}] {path}")
    return exists


def main():
    section("1. DIRECTORY STRUCTURE")
    required_dirs = [
        "client/src",
        "gateway/src",
        "worker/src",
        "proto",
        "config",
        "docker",
    ]
    for d in required_dirs:
        check_dir(d)

    section("2. CHECK __init__.py FILES IN proto/ PACKAGES")
    check_file("gateway/src/proto/__init__.py")
    check_file("worker/src/proto/__init__.py")

    section("3. CHECK PROTO FILES EXIST")
    check_file("proto/sensor.proto")

    section("4. CHECK GENERATED gRPC FILES")
    check_file("gateway/src/proto/sensor_pb2.py")
    check_file("gateway/src/proto/sensor_pb2_grpc.py")
    check_file("worker/src/proto/sensor_pb2.py")
    check_file("worker/src/proto/sensor_pb2_grpc.py")

    section("5. TRY IMPORTING GENERATED MODULES")
    sys.path.append(os.path.join(ROOT, "gateway/src"))
    sys.path.append(os.path.join(ROOT, "worker/src"))

    try:
        import proto.sensor_pb2 as g_pb2
        import proto.sensor_pb2_grpc as g_grpc
        print("[OK] Gateway proto imports work")
    except Exception as e:
        print("[FAIL] Gateway proto import error:", e)

    try:
        import proto.sensor_pb2 as w_pb2
        import proto.sensor_pb2_grpc as w_grpc
        print("[OK] Worker proto imports work")
    except Exception as e:
        print("[FAIL] Worker proto import error:", e)

    section("6. CHECK config.yaml LOADS")
    try:
        cfg_path = os.path.join(ROOT, "config/config.yaml")
        with open(cfg_path, "r") as f:
            data = yaml.safe_load(f)
        print("[OK] config.yaml loads successfully")
        print("Student ID:", data.get("student_id"))
    except Exception as e:
        print("[FAIL] Error loading config.yaml:", e)

    section("7. SUMMARY")
    print("If all items above are OK, you are good to run docker compose.")


if __name__ == "__main__":
    main()
