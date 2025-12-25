from __future__ import annotations

import argparse
import logging

from src.config.settings import load_settings
from src.pipeline.uci_runner import run_uci_pipeline
from src.pipeline.aqicn_runner import run_aqicn_pipeline


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("pip")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AQI Pipeline (UCI core + AQICN bonus)")
    p.add_argument("--mode", choices=["uci", "aqicn"], default="uci", help="Execution mode")
    return p



def main() -> None:
    settings = load_settings()
    args = build_parser().parse_args()
    print(f"AQICN API token: {settings.aqicn_api_token}")
    try:
        if args.mode == "uci":
            run_uci_pipeline(
                uci_csv=settings.uci_csv_path,
                onnx_out=settings.models_dir / "uci_co_model.onnx",
                plot_out=settings.plots_dir / "uci_actual_vs_pred.png",
            )
        else:
            run_aqicn_pipeline(
                api_token=settings.aqicn_api_token,
                db_path=settings.aqicn_db_path,
                plots_dir=settings.plots_dir,
                cities=settings.cities,
            )

    except Exception as e:
        logger.exception("Fatal error: %s", e)
        raise


if __name__ == "__main__":
    main()
