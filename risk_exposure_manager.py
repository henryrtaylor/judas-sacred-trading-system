
def adjust_fixed_lot(fixed_lot, total_exposure, risk_threshold=0.2):
    if total_exposure < risk_threshold * 0.5:
        return fixed_lot * 1.5
    elif total_exposure > risk_threshold:
        return fixed_lot * 0.5
    return fixed_lot
