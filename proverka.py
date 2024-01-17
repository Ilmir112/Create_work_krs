def remove_overlapping_intervals(perforating_intervals):

    from open_pz import CreatePZ
    CreatePZ.current_bottom = 1470
    print(f' перфорация_ {perforating_intervals}')
    skipping_intervals = []
    for pvr in sorted(perforating_intervals, key = lambda x: x[0]):
        if pvr[1] <= CreatePZ.current_bottom - 3:
            if pvr[1] + 40 < CreatePZ.current_bottom and pvr[0] < CreatePZ.current_bottom:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                skipping_intervals.append([pvr[1] + 2, pvr[1] + 40])

            elif pvr[1] + 40 > CreatePZ.current_bottom and pvr[0] < CreatePZ.current_bottom:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                skipping_intervals.append([pvr[1] + 2, CreatePZ.current_bottom - 2])

    print(f'СКМ на основе ПВР{skipping_intervals}')
    lll = []
    for skm in sorted(skipping_intervals, key = lambda x: x[0]):
        kroly_skm = skm[0]
        pod_skm = skm[1]

        for pvr in sorted(perforating_intervals, key = lambda x: x[0]):
            if abs(pvr[0]-skm[0]) < 90 or abs(pvr[1]-skm[1]) <=40:
                kroly_skm_pvr = pvr[0]
                pod_skm_pvr = pvr[1]
                True_pod = kroly_skm <= pod_skm_pvr <= pod_skm
                true_krov = kroly_skm <= kroly_skm_pvr <= pod_skm

                if True_pod and true_krov:
                    if skm in skipping_intervals:
                        skipping_intervals.remove(skm)
                        if any([kroly_skm < pvr[0] < pvr[0]-2 or pvr[1] < pvr[1] < skm[1] for pvr in perforating_intervals]) == False and kroly_skm>pod_skm:
                            skipping_intervals.append((kroly_skm, pvr[0]-2))
                            skipping_intervals.append((pvr[1] + 2, pod_skm))
                    #     lll.append((pvr[1] + 2, skm[1]))
                    # print(f' {skm} {pvr} перв {lll}')

                elif true_krov is False and True_pod:
                    if skm in skipping_intervals:
                        if any([(skm[0] < pvr[0] < skm[1] or skm[0] < pvr[1] < pvr[0]-2) for pvr in perforating_intervals]) == False and kroly_skm>pod_skm:
                            skipping_intervals.remove(skm)
                            skipping_intervals.append((skm[0], pvr[0]-2))
                    # lll.append((skm[0], pvr[0]-2))
                    #
                    # print(f' {skm} {pvr} втор {lll}')

                elif True_pod and true_krov is False:
                    if skm in skipping_intervals:
                        if any([(skm[0] < pvr[0] < skm[1] or pvr[1] + 2 < pvr[1] < skm[1]) for pvr in
                                perforating_intervals]) == False and kroly_skm>od_skm:
                            skipping_intervals.remove(skm)
                            skipping_intervals.append((pvr[1] + 2, skm[1]))
                    # lll.append((pvr[1] + 2, skm[1]))
                    # print(f' {skm} {pvr} третий {lll}')
                # else:
                #
                #     if skm not in lll:
                #         lll.append((skm[0], skm[1]))
                #     print(f' {skm} {pvr} четв {lll}')

    print(all([kroly_skm <= pvr[1] <= pod_skm or kroly_skm <= pvr[0] <= pod_skm for pvr in perforating_intervals]))

    skipping_intervals = sorted(skipping_intervals, key=lambda x: x[0])



    print(f'после разделения {skipping_intervals}')



    # for skm in sorted(skipping_intervals, key = lambda x: x[0]):
    #     for pvr in sorted(perforating_intervals, key = lambda x: x[0]):
    #         if skm in skipping_intervals:
    #             if skm[0] < pvr[0] or skm[1] > skm[0] or skm[1] > pvr[1]+1:
    #                 skipping_intervals.remove(skm)
    # print(f' после удаления {skipping_intervals}')
    return skipping_intervals

perforating_intervals =   [[851.0, 856.0], [974.0, 978.0], [956.0, 960.0], [962.0, 964.0], [1022.0, 1031.0], [1459.0, 1461.0]]

print(remove_overlapping_intervals(perforating_intervals))