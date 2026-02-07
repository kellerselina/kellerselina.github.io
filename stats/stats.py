# %% 

import os
import sys
import shutil
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path as path

def in_interactive() -> bool:
	"""
		check if running in interactive mode (jupyter, ipython, etc).
	"""
	return hasattr(sys, 'ps1') or 'ipykernel' in sys.modules or 'IPython' in sys.modules

def setup_matplotlib():
	"""
		configure matplotlib for publication-quality plots
		(uses LaTeX rendering if pdflatex is available, otherwise standard rendering).
	"""
	config = {
		"font.size": 8,
		"font.family": "serif",
		"font.serif": ["CMU Serif"],
		"figure.dpi": 150,
	}
	if shutil.which("pdflatex"):
		config.update({
			"pgf.texsystem": "pdflatex",
			"text.usetex": True,
			"text.latex.preamble": r"\usepackage{amsfonts}\usepackage{mathtools}\usepackage{bm}"
		})
	plt.rcParams.update(config)

def date_xlsx(in_file: str) -> str:
	"""
		read raw excel data and return last Work Date as YYYY-MM-DD.
	"""
	df = pd.read_excel(in_file, sheet_name = 0)
	if "Work Date" not in df.columns:
		raise ValueError("missing 'Work Date' column in xlsx.")
	dt = pd.to_datetime(df["Work Date"], errors = "coerce").dropna()
	if dt.empty:
		raise ValueError("no valid dates found in 'Work Date' column.")
	return dt.max().strftime("%Y-%m-%d")

def raw_data_to_csv(in_file: str, out_file: str):
	"""
		read raw excel data from "in_file", clean it, and write to "out_file" as csv.

		inputs:
			in_file  = path to raw excel data file
			out_file = path to cleaned csv output file
	"""
	df = pd.read_excel(in_file, sheet_name = 0)
	# select cols
	df_clean = (
		df[["Work Date", "Work Hours", "Work Type"]].rename(columns = {
			"Work Date": "date",
			"Work Hours": "hours",
			"Work Type": "type",
		}))
	# clean date, hours
	df_clean["date"] = pd.to_datetime(df_clean["date"], errors = "coerce").dt.strftime("%Y-%m-%d")
	df_clean["hours"] = pd.to_numeric(df_clean["hours"], errors = "coerce")
	# clean/map type
	type_map = {
		"OTH":  "others",
		"BIL":  "billable",
		"PSQ":  "pro_bono",
		"REC":  "recruitment",
		"MAN":  "management",
		"ADM":  "administrative",
		"PD":   "practice_development",
		"SICK": "sick",
		"VAC":  "vacation",
	}
	code = df_clean["type"].astype(str).str.strip().str.upper()
	mapped = code.map(type_map)
	df_clean["type"] = mapped.fillna(code.str.lower())
	# drop rows with missing date, hours, type
	df_clean = df_clean.dropna(subset = ["date", "hours", "type"])
	df_clean.to_csv(out_file, index = False)
	print(f"\nwrote {path(out_file).resolve()}{os.sep} with {len(df_clean)} rows.")

def csv_to_bm(csv_file: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
	"""
	read cleaned csv file and aggregate hours for relevant types.

	returns:
		df_weekly   = columns ["week", "hours"]
		df_biweekly = columns ["two_weeks", "hours"]  (14-day bins)
		df_monthly  = columns ["month", "hours"]   (label "yyyy-mm")
	"""
	keep_types = {
		"billable",
		"pro_bono",
		"recruitment",
		"management",
		"practice_development",
	}
	df = pd.read_csv(csv_file)
	df = df[df["type"].isin(keep_types)].copy()
	df["date"] = pd.to_datetime(df["date"], errors = "coerce")
	df = df.dropna(subset = ["date", "hours"])
	# weekly
	df_weekly = (
		df.set_index("date")["hours"]
		.resample("W-MON", label = "left", closed = "left").sum()
		.reset_index()
		.rename(columns = {"date": "week"})
	)
	df_weekly["week"] = df_weekly["week"].dt.strftime("%Y-%m-%d")
	# biweekly (14-day bins)
	df_biweekly = (
		df.set_index("date")["hours"]
		.resample("2W-MON").sum()
		.reset_index()
		.rename(columns={"date": "two_weeks"})
	)
	df_biweekly["two_weeks"] = df_biweekly["two_weeks"].dt.strftime("%Y-%m-%d")
	# monthly (label without day)
	df_monthly = (
		df.set_index("date")["hours"]
		.resample("MS").sum()
		.reset_index()
		.rename(columns = {"date": "month"})
	)
	df_monthly["month"] = df_monthly["month"].dt.strftime("%Y-%m")
	return df_weekly, df_biweekly, df_monthly

def plot_df(df: pd.DataFrame, labels: tuple[str, str], n_ticks: int = 0, figsize: tuple[float, float] = (12, 4), out_file: str | None = None) -> None:
	"""
	plot a two-columns dataframe.

	inputs:
		df        = dataframe with two columns
		labels    = tuple of x and y axis labels
		n_ticks   = number of x ticks to show
		figsize   = figsize tuple
		out_file  = optional path to save figure
	"""
	if df.shape[1] != 2:
		raise ValueError("df must have exactly two columns.")
	x_col, y_col = df.columns
	setup_matplotlib()
	fig = plt.figure(figsize = figsize)
	plt.plot(df[x_col], df[y_col], linewidth = 1., color = "black")
	plt.margins(x = 0)
	x_label = (r"$" + labels[0] + r"$" if shutil.which("pdflatex") else labels[0]) + " (" + str(x_col) + ")"
	y_label = (r"$" + labels[1] + r"$" if shutil.which("pdflatex") else labels[1]) + " (" + str(y_col) + ")"
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	grid = plt.grid(visible = True, which = "both", linestyle = "--", linewidth = 0.75, alpha = 0.25)
	if n_ticks == -1:
		plt.xticks(rotation = 30, ha = "right")
	elif (n_ticks == 0) or (n_ticks == 1):
		plt.xticks([])
	elif (len(df) > n_ticks) and (n_ticks > 1):
		idx = [int(i * (len(df) - 1) / (n_ticks - 1)) for i in range(n_ticks)]
		plt.xticks(df[x_col].iloc[idx], rotation = 30, ha = "right")
	if out_file is not None:
		fig.savefig(out_file, bbox_inches = "tight")
		print(f"saved figure {path(out_file).resolve()}{os.sep}")
	if in_interactive():
		plt.show()
	plt.close(fig)

def main():
	in_path = input("enter .xlsx path (it should be in the same directory as this script): ").strip().strip('"')
	if not in_path:
		raise ValueError("no input file provided.")
	in_file = path(in_path)
	if not in_file.exists():
		raise ValueError(f"file '{in_file}' not found.")
	if in_file.suffix.lower() != ".xlsx":
		raise ValueError("input file must be .xlsx.")
	date_str = date_xlsx(str(in_file))
	target_name = f"keller_db_{date_str}.xlsx"
	target_path = path.cwd() / target_name
	if in_file.resolve() != target_path.resolve():
		if target_path.exists():
			raise ValueError(f"target '{target_path}' already exists.")
		shutil.move(str(in_file), str(target_path))
	in_file = target_path
	date_dir = path(date_str)
	date_dir.mkdir(parents = True, exist_ok = True)
	out_file = str(date_dir / f"keller_db_{date_str}.csv")
	raw_data_to_csv(str(in_file), out_file)
	weekly_hours, biweekly_hours, monthly_hours = csv_to_bm(out_file)
	fig_dir = date_dir / "figures"
	fig_dir.mkdir(parents = True, exist_ok = True)
	data_map = {
		"week": weekly_hours,
		"two_weeks": biweekly_hours,
		"month": monthly_hours,
	}
	size_map = {
		"week": (24, 6),
		"two_weeks": (12, 6),
		"month": (8, 6),
	}
	for base, df in data_map.items():
		figsize = size_map.get(base)
		plot_path = str(fig_dir / f"billable_hours_{base}_plot.pdf")
		csv_path = str(fig_dir / f"billable_hours_{base}_table.csv")
		plot_df(df, labels = ("t", "h"), n_ticks = -1, figsize = figsize, out_file = plot_path)
		df.to_csv(csv_path, index = False)
		print(f"wrote {path(csv_path).resolve()}{os.sep} with {len(df)} rows.")
		if in_interactive():
			display(df)
	input("\npress enter to exit.")
	
if __name__ == "__main__":
	main()

# %%
