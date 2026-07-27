# Indicator Creation and Drawing Constants

## ENUM_INDICATOR — Used with `IndicatorCreate(sym, tf, type, params[])`

| Value | Indicator | Value | Indicator |
|-------|-----------|-------|-----------|
| `IND_AC` | Accelerator Oscillator | `IND_MA` | Moving Average |
| `IND_AD` | Accumulation/Distribution | `IND_MACD` | MACD |
| `IND_ADX` | Average Directional Index | `IND_MFI` | Money Flow Index |
| `IND_ADXW` | ADX (Welles Wilder) | `IND_MOMENTUM` | Momentum |
| `IND_ALLIGATOR` | Alligator | `IND_OBV` | On Balance Volume |
| `IND_AMA` | Adaptive Moving Average | `IND_OSMA` | OsMA |
| `IND_AO` | Awesome Oscillator | `IND_RSI` | RSI |
| `IND_ATR` | Average True Range | `IND_RVI` | Relative Vigor Index |
| `IND_BANDS` | Bollinger Bands | `IND_SAR` | Parabolic SAR |
| `IND_BEARS` | Bears Power | `IND_STDDEV` | Standard Deviation |
| `IND_BULLS` | Bulls Power | `IND_STOCHASTIC` | Stochastic Oscillator |
| `IND_BWMFI` | Market Facilitation Index | `IND_TEMA` | Triple EMA |
| `IND_CCI` | Commodity Channel Index | `IND_TRIX` | TRIX |
| `IND_CHAIKIN` | Chaikin Oscillator | `IND_VIDYA` | VIDYA |
| `IND_DEMA` | Double EMA | `IND_VOLUMES` | Volumes |
| `IND_DEMARKER` | DeMarker | `IND_WPR` | Williams' %R |
| `IND_ENVELOPES` | Envelopes | `IND_FRAMA` | Fractal Adaptive MA |
| `IND_FORCE` | Force Index | `IND_GATOR` | Gator Oscillator |
| `IND_FRACTALS` | Fractals | `IND_ICHIMOKU` | Ichimoku |
| `IND_CUSTOM` | Custom indicator | | |

> For `IND_CUSTOM`, the first `MqlParam` element must be `TYPE_STRING` with
> `string_value` = custom indicator name.

## Indicator Buffer Line Constants — For `CopyBuffer(handle, buffer_index, ...)`

| Constant | Value | Used with |
|----------|-------|-----------|
| `MAIN_LINE` | 0 | iMACD, iRVI, iStochastic (main line) |
| `SIGNAL_LINE` | 1 | iMACD, iRVI, iStochastic (signal) |
| `PLUSDI_LINE` | 1 | iADX, iADXW (+DI line) |
| `MINUSDI_LINE` | 2 | iADX, iADXW (-DI line) |
| `BASE_LINE` | 0 | iBands (middle band) |
| `UPPER_BAND` | 1 | iBands (upper band) |
| `LOWER_BAND` | 2 | iBands (lower band) |

## ENUM_DRAW_TYPE — Custom Indicator Drawing Style

| Value | Data bufs | Description |
|-------|-----------|-------------|
| `DRAW_NONE` | 1 | Not drawn |
| `DRAW_LINE` | 1 | Simple line |
| `DRAW_SECTION` | 1 | Line sections (gaps at empty values) |
| `DRAW_HISTOGRAM` | 1 | Histogram from zero |
| `DRAW_HISTOGRAM2` | 2 | Histogram between two buffers |
| `DRAW_ARROW` | 1 | Arrow symbols |
| `DRAW_ZIGZAG` | 2 | ZigZag |
| `DRAW_FILLING` | 2 | Colour fill between two buffers |
| `DRAW_BARS` | 4 | Bars (OHLC) |
| `DRAW_CANDLES` | 4 | Candlesticks |
| `DRAW_COLOR_LINE` | 1+1 | Multicoloured line |
| `DRAW_COLOR_HISTOGRAM` | 1+1 | Multicoloured histogram |
| `DRAW_COLOR_HISTOGRAM2` | 2+1 | Multicoloured histogram2 |
| `DRAW_COLOR_ARROW` | 1+1 | Multicoloured arrows |
| `DRAW_COLOR_ZIGZAG` | 2+1 | Multicoloured ZigZag |
| `DRAW_COLOR_BARS` | 4+1 | Multicoloured bars |
| `DRAW_COLOR_CANDLES` | 4+1 | Multicoloured candles |

> `+1` = additional colour index buffer required after data buffers.

## ENUM_INDEXBUFFER_TYPE — `SetIndexBuffer(index, buffer[], type)`

| Value | Description |
|-------|-------------|
| `INDICATOR_DATA` | Drawing data buffer |
| `INDICATOR_COLOR_INDEX` | Colour index buffer (for COLOR_ draw types) |
| `INDICATOR_CALCULATIONS` | Auxiliary calculation buffer (not drawn) |
