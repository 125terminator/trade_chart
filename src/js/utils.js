export async function copyToClipboard(mytext) {
    try {
        await navigator.clipboard.writeText(mytext);
    } catch ($e) {
    }
}

export function lower_bound(arr, x) {
    var l = 0, r = arr.length, m, near_val = arr[0][0];
    while (l < r) {
        m = parseInt((l + r) / 2);
        if (arr[m][0] == x) {
            return [m, arr[m][0]]
        }
        if (arr[m][0] < x) {
            near_val = arr[m][0];
            l = m + 1;
        } else {
            r = m;
        }
    }
    return [l, near_val];
}

export function tf_to_ms(tf) {
    let multiply_factor = 1
    if (tf.includes('m')) {
        multiply_factor = 60000
    }
    else if (tf.includes('H')) {
        multiply_factor = 3600000
    }
    else if (tf.includes('D')) {
        multiply_factor = 86400000
    }
    return parseInt(tf) * multiply_factor
}

export function cal_intra(bp, sp, qty) {
    bp = parseFloat(bp.toFixed(2));
    sp = parseFloat(sp.toFixed(2));
    qty = parseFloat(qty.toFixed(2));

    if (isNaN(qty) || (isNaN(bp) && isNaN(sp))) {
        return;
    }
    if (isNaN(bp) || bp == 0) {
        bp = 0;
        bse_tran_charge_buy = 0;
    }
    if (isNaN(sp) || sp == 0) {
        sp = 0;
        bse_tran_charge_sell = 0;
    }
    var brokerage_buy = ((bp * qty * 0.0003) > 20) ? 20 : parseFloat(parseFloat(bp * qty * 0.0003).toFixed(2));
    var brokerage_sell = ((sp * qty * 0.0003) > 20) ? 20 : parseFloat(parseFloat(sp * qty * 0.0003).toFixed(2));
    var brokerage = parseFloat(parseFloat(brokerage_buy + brokerage_sell).toFixed(2));

    var turnover = parseFloat(parseFloat((bp + sp) * qty).toFixed(2));

    var stt_total = Math.round(parseFloat(parseFloat((sp * qty) * 0.00025).toFixed(2)));

    var exc_trans_charge = parseFloat(parseFloat(0.0000345 * turnover).toFixed(2));
    var cc = 0;

    var stax = parseFloat(parseFloat(0.18 * (brokerage + exc_trans_charge)).toFixed(2));

    var sebi_charges = parseFloat(parseFloat(turnover * 0.000001).toFixed(2));
    sebi_charges = parseFloat(parseFloat(sebi_charges + (sebi_charges * 0.18)).toFixed(2));

    var stamp_charges = Math.round(parseFloat(parseFloat((bp * qty) * 0.00003).toFixed(2)));

    var total_tax = parseFloat(parseFloat(brokerage + stt_total + exc_trans_charge + cc + stax + sebi_charges + stamp_charges).toFixed(2));

    var breakeven = parseFloat(parseFloat(total_tax / qty).toFixed(2));
    breakeven = isNaN(breakeven) ? 0 : breakeven

    var net_profit = parseFloat(parseFloat(((sp - bp) * qty) - total_tax).toFixed(2));

    return [net_profit, total_tax]
}

function cal_delivery(bp, sp, qty) {
    bp = parseFloat(bp.toFixed(2));
    sp = parseFloat(sp.toFixed(2));
    qty = parseFloat(qty.toFixed(2));


    if (isNaN(qty) || (isNaN(bp) && isNaN(sp))) {
        return;
    }
    if (isNaN(bp) || bp == 0) {
        bp = 0;
        bse_tran_charge_buy = 0;
    }
    if (isNaN(sp) || sp == 0) {
        sp = 0;
        bse_tran_charge_sell = 0;
    }

    var turnover = parseFloat(parseFloat((bp + sp) * qty).toFixed(2));

    var brokerage = 0;

    var stt_total = Math.round(parseFloat(parseFloat(turnover * 0.001).toFixed(2)));

    var exc_trans_charge = (document.getElementsByClassName("del_nse")[0].checked) ? parseFloat(parseFloat(0.0000345 * turnover).toFixed(2)) : parseFloat(parseFloat(0.0000345 * turnover).toFixed(2));
    var cc = 0;
    var dp = 15.93;
    if (sp == 0) dp = 0

    var stax = parseFloat(parseFloat(0.18 * (brokerage + exc_trans_charge)).toFixed(2));

    var sebi_charges = parseFloat(parseFloat(turnover * 0.000001).toFixed(2));
    sebi_charges = parseFloat(parseFloat(sebi_charges + (sebi_charges * 0.18)).toFixed(2));

    var stamp_charges = Math.round(parseFloat(parseFloat(bp * qty * 0.00015).toFixed(2)));

    var total_tax = parseFloat(parseFloat(brokerage + stt_total + exc_trans_charge + cc + dp + stax + sebi_charges + stamp_charges).toFixed(2));

    var breakeven = parseFloat(parseFloat(total_tax / qty).toFixed(2));
    breakeven = isNaN(breakeven) ? 0 : breakeven

    var net_profit = parseFloat(parseFloat(((sp - bp) * qty) - total_tax).toFixed(2));

    return net_profit
}