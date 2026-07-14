Grid {
        grid-size: 2 6;        /* 2 columns, 6 rows */
        grid-columns: auto 1fr;
        grid-rows: 3 3 3 1 1fr 3;
        padding: 1 2;
    }

#row1-label, #row2-label {
        content-align: right middle;
        padding-right: 1;
    }

    #add-btn {
        column-span: 2;
        width: 100%;
    }

    #spacer {
        column-span: 2;
    }

    #fund-table {
        column-span: 2;
        height: 100%;
    }

    #footer-box {
        column-span: 2;
        border: round $accent;
        content-align: center middle;
        height: 100%;
    }

/* This is for the stock delete confirmation dialog */
#butons {
	width: 100%;
	align-horizontal: right;
	margin-top: 1;
}

#dialog {
	width: 40;

	padding: 1 2;
	border: thick $primary;
	background: $surface;

	align-horizontal: center;
}

DeleteStockScreen {
	align: center middle;
}
